from llama_index.core import Document, VectorStoreIndex

documents = [
    Document(text="Bug detection agent reviews code for logic issues."),
    Document(text="Security reviewer analyzes vulnerabilities."),
    Document(text="Performance reviewer identifies bottlenecks.")
]

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query(
    "What does the security reviewer do?"
)

print(response)