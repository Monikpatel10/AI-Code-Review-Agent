"""RAG Knowledge Base — stores known vulnerability patterns, best practices,
and common bug patterns for retrieval-augmented code review.

Uses ChromaDB for vector storage and sentence-transformers embeddings.
"""

from __future__ import annotations

import logging
import os

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings
from app.llm.hf_client import HuggingFaceClient

logger = logging.getLogger(__name__)

BUILTIN_KNOWLEDGE = [
    {
        "id": "sec-sqli",
        "category": "security",
        "title": "SQL Injection (CWE-89)",
        "content": "SQL injection occurs when user input is directly concatenated into SQL queries. "
                   "Look for string formatting/f-strings in SQL, cursor.execute() with format strings. "
                   "Fix: use parameterized queries with placeholders (%s, ?, :param).",
        "languages": ["python", "javascript", "java", "php"],
    },
    {
        "id": "sec-xss",
        "category": "security",
        "title": "Cross-Site Scripting / XSS (CWE-79)",
        "content": "XSS occurs when user input is rendered in HTML without escaping. "
                   "Look for innerHTML, document.write, dangerouslySetInnerHTML, |safe filter. "
                   "Fix: escape output, use textContent, use CSP headers.",
        "languages": ["javascript", "typescript", "python", "php"],
    },
    {
        "id": "sec-cmdi",
        "category": "security",
        "title": "Command Injection (CWE-78)",
        "content": "Command injection occurs when user input flows into os.system(), subprocess with shell=True, "
                   "child_process.exec(). Fix: use subprocess with list args (shell=False), shlex.quote().",
        "languages": ["python", "javascript", "ruby"],
    },
    {
        "id": "sec-path-traversal",
        "category": "security",
        "title": "Path Traversal (CWE-22)",
        "content": "Path traversal lets attackers access files outside the intended directory using ../ sequences. "
                   "Look for os.path.join with user input, open() with user-controlled paths. "
                   "Fix: use os.path.realpath() and verify the resolved path starts with the base directory.",
        "languages": ["python", "javascript", "java"],
    },
    {
        "id": "sec-deserialization",
        "category": "security",
        "title": "Insecure Deserialization (CWE-502)",
        "content": "Insecure deserialization with pickle.loads(), yaml.load() (without SafeLoader), "
                   "or eval() on untrusted data can lead to remote code execution. "
                   "Fix: use json, yaml.safe_load(), or a whitelist-based deserializer.",
        "languages": ["python", "java", "php"],
    },
    {
        "id": "sec-hardcoded-secrets",
        "category": "security",
        "title": "Hardcoded Credentials (CWE-798)",
        "content": "Passwords, API keys, and tokens hardcoded in source code are exposed if the repo is public. "
                   "Look for variable names like password, secret, api_key, token assigned to string literals. "
                   "Fix: use environment variables, secrets manager, or config files not in version control.",
        "languages": ["python", "javascript", "java", "go"],
    },
    {
        "id": "perf-n-plus-1",
        "category": "performance",
        "title": "N+1 Query Problem",
        "content": "N+1 queries occur when code makes one query to fetch a list, then one query per item. "
                   "Look for database queries inside for-loops, ORM lazy loading in loops. "
                   "Fix: use eager loading (select_related/prefetch_related in Django, joinedload in SQLAlchemy).",
        "languages": ["python", "javascript", "ruby", "java"],
    },
    {
        "id": "perf-quadratic",
        "category": "performance",
        "title": "Quadratic or Worse Complexity",
        "content": "Nested loops over the same collection give O(n²) complexity. List membership tests "
                   "with `in` inside loops also cause quadratic behavior. "
                   "Fix: use sets/dicts for O(1) lookups, sort-based approaches, or built-in functions.",
        "languages": ["python", "javascript", "java"],
    },
    {
        "id": "perf-string-concat",
        "category": "performance",
        "title": "String Concatenation in Loop",
        "content": "Building strings with += in a loop creates O(n²) allocations in many languages. "
                   "Fix: use str.join(), StringBuilder, list append + join, or f-strings.",
        "languages": ["python", "javascript", "java"],
    },
    {
        "id": "bug-mutable-default",
        "category": "bug",
        "title": "Mutable Default Arguments (Python)",
        "content": "Using mutable objects (list, dict, set) as default function arguments causes the same "
                   "object to be shared across all calls. Fix: use None as default, create new object in body.",
        "languages": ["python"],
    },
    {
        "id": "bug-late-binding",
        "category": "bug",
        "title": "Late Binding Closures",
        "content": "Lambda/closures in loops capture variables by reference, not by value. "
                   "All closures end up referencing the last value of the loop variable. "
                   "Fix: use default argument (lambda x=x: ...) or functools.partial.",
        "languages": ["python", "javascript"],
    },
    {
        "id": "bug-equality-vs-identity",
        "category": "bug",
        "title": "Equality vs Identity Comparison",
        "content": "Using `is` to compare values instead of `==` works only for small integers and interned strings. "
                   "Use `==` for value comparison, `is` only for None/True/False/sentinel objects.",
        "languages": ["python"],
    },
    {
        "id": "bp-solid",
        "category": "best_practice",
        "title": "SOLID Principles",
        "content": "S: Single Responsibility — each class/function does one thing. "
                   "O: Open/Closed — extend via composition, not modification. "
                   "L: Liskov Substitution — subtypes must be substitutable. "
                   "I: Interface Segregation — small focused interfaces. "
                   "D: Dependency Inversion — depend on abstractions, not concretions.",
        "languages": ["python", "javascript", "java", "typescript"],
    },
    {
        "id": "bp-error-handling",
        "category": "best_practice",
        "title": "Proper Error Handling",
        "content": "Catch specific exceptions, not bare except or catch(Exception). "
                   "Log errors with context. Don't swallow exceptions silently. "
                   "Use finally/context managers for cleanup. Fail fast on unrecoverable errors.",
        "languages": ["python", "javascript", "java"],
    },
]


def load_rag_docs() -> list[dict]:
    """Load external markdown RAG documents from data/rag_docs."""
    rag_dir = os.path.join("data", "rag_docs")
    entries = []

    if not os.path.exists(rag_dir):
        return entries

    file_category_map = {
        "security_rules.md": "security",
        "performance_rules.md": "performance",
        "style_rules.md": "style",
        "bug_patterns.md": "bug",
    }

    for filename, category in file_category_map.items():
        path = os.path.join(rag_dir, filename)

        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            continue

        sections = content.split("\n## ")

        for index, section in enumerate(sections):
            section = section.strip()

            if not section or section.startswith("# "):
                continue

            lines = section.splitlines()
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

            entries.append({
                "id": f"rag-{category}-{index}",
                "category": category,
                "title": title,
                "content": body,
                "languages": ["python", "javascript", "java", "typescript"],
            })

    return entries


class KnowledgeBase:
    """Manages the ChromaDB vector store for RAG-enhanced code review."""

    def __init__(self, llm: HuggingFaceClient):
        self.llm = llm
        persist_dir = settings.chroma_persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self._client = chromadb.Client(ChromaSettings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory=persist_dir,
        ))

        self._collection = self._client.get_or_create_collection(
            name="code_review_knowledge",
            metadata={"hnsw:space": "cosine"},
        )

        self._initialized = False

    async def initialize(self):
        """Seed the knowledge base with built-in patterns + external RAG docs if empty."""
        if self._initialized:
            return

        external_knowledge = load_rag_docs()
        all_knowledge = BUILTIN_KNOWLEDGE + external_knowledge

        existing = self._collection.count()
        if existing >= len(all_knowledge):
            self._initialized = True
            return

        logger.info("Seeding knowledge base with %d entries…", len(all_knowledge))

        ids = [entry["id"] for entry in all_knowledge]

        documents = [
            f"[{entry['category'].upper()}] {entry['title']}\n{entry['content']}"
            for entry in all_knowledge
        ]

        metadatas = [
            {"category": entry["category"], "languages": ",".join(entry["languages"])}
            for entry in all_knowledge
        ]

        try:
            embeddings = self.llm.embed(documents)
            self._collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            logger.info("Knowledge base seeded successfully with external RAG docs.")
        except Exception as exc:
            logger.warning("Failed to seed knowledge base with embeddings: %s", exc)
            self._collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )

        self._initialized = True

    async def add_custom_entry(
        self,
        entry_id: str,
        category: str,
        title: str,
        content: str,
        languages: list[str],
    ):
        """Add a custom knowledge entry."""
        doc = f"[{category.upper()}] {title}\n{content}"

        try:
            embeddings = self.llm.embed([doc])
            self._collection.upsert(
                ids=[entry_id],
                documents=[doc],
                embeddings=embeddings,
                metadatas=[{"category": category, "languages": ",".join(languages)}],
            )
        except Exception:
            self._collection.upsert(
                ids=[entry_id],
                documents=[doc],
                metadatas=[{"category": category, "languages": ",".join(languages)}],
            )

    async def query(self, code_snippet: str, language: str, top_k: int = 5) -> list[str]:
        """Retrieve the most relevant knowledge entries for a code snippet."""
        await self.initialize()

        try:
            embeddings = self.llm.embed([code_snippet])
            results = self._collection.query(
                query_embeddings=embeddings,
                n_results=top_k,
                where={"languages": {"$contains": language}} if language != "unknown" else None,
            )
        except Exception:
            results = self._collection.query(
                query_texts=[code_snippet],
                n_results=top_k,
            )

        documents = results.get("documents", [[]])[0]
        return documents


class RAGRetriever:
    """High-level retriever that formats knowledge base results as context for prompts."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    async def retrieve_context(self, code: str, language: str) -> str:
        """Retrieve and format relevant patterns as context string."""
        snippet = code[:500]
        docs = await self.kb.query(snippet, language, top_k=settings.rag_top_k)

        if not docs:
            return ""

        sections = []
        for i, doc in enumerate(docs, 1):
            sections.append(f"{i}. {doc}")

        return "\n\n".join(sections)