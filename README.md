# Multi-Agent AI Code Review System

Built and maintained by Monik Patel

> Multi-agent AI-powered code review platform that integrates directly into VS Code using local and cloud-hosted LLMs, Retrieval-Augmented Generation (RAG), semantic code retrieval, and specialized reviewer agents. Built with FastAPI, LangChain, LangGraph, ChromaDB, FAISS, LlamaIndex, AutoGen, Ollama, Hugging Face, OpenAI APIs, and a custom C++ vector retrieval engine.

---

## Overview

The Multi-Agent AI Code Review System automates software quality analysis by combining static analysis, semantic retrieval, and LLM-powered reasoning. The platform coordinates specialized reviewer agents to identify bugs, security vulnerabilities, performance bottlenecks, and maintainability issues while providing grounded recommendations through Retrieval-Augmented Generation (RAG).

The system supports both local inference through Ollama and cloud-hosted LLM services, allowing developers to run reviews in privacy-sensitive environments or leverage larger hosted models.

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    VS Code Extension                         │
│                                                             │
│  Commands • Diagnostics • Quick Fixes • Dashboard          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│                                                             │
│               Multi-Agent Orchestrator                      │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │   Bug    │ │ Security │ │  Perf    │ │  Style   │      │
│  │ Detector │ │ Analyzer │ │ Reviewer │ │ Checker  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│                                                             │
│       Consensus • Deduplication • Ranking                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  RAG Retrieval Layer                        │
│                                                             │
│  ChromaDB • FAISS • Hugging Face Embeddings                │
│  LlamaIndex • Semantic Search • Context Retrieval          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Providers                            │
│                                                             │
│  Ollama • Hugging Face • OpenAI                            │
│                                                             │
│  Qwen2.5-Coder • CodeLlama • DeepSeek-Coder                │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features

### Multi-Agent Review System

Specialized reviewer agents independently analyze code and collaborate through an orchestration layer.

#### Bug Detector
- Logical errors
- Null reference issues
- Off-by-one mistakes
- Resource management problems

#### Security Analyzer
- OWASP Top 10 vulnerabilities
- CWE-mapped findings
- Injection vulnerabilities
- Hardcoded secrets

#### Performance Reviewer
- N+1 query detection
- Algorithmic inefficiencies
- Memory usage concerns
- Scalability bottlenecks

#### Style Checker
- Naming conventions
- SOLID principles
- Code duplication
- Maintainability issues

#### Orchestrator
- Multi-agent coordination
- Consensus scoring
- Finding deduplication
- Confidence ranking

---

## Retrieval-Augmented Generation (RAG)

The review system uses Retrieval-Augmented Generation to ground AI responses in domain-specific knowledge.

### Components

- ChromaDB vector database
- FAISS similarity search
- Hugging Face embedding models
- Semantic retrieval pipelines
- Dynamic context injection

### Benefits

- Reduced hallucinations
- More consistent findings
- Repository-aware recommendations
- Explainable review output

### Knowledge Sources

- Security vulnerability patterns
- Performance optimization rules
- Bug detection heuristics
- Software engineering best practices
- Style and maintainability guidelines

---

## Agent Orchestration

The platform leverages modern agent frameworks to coordinate review workflows.

### LangGraph

Used to orchestrate review workflows and manage execution paths between specialized reviewer agents.

### LangChain

Used for prompt construction, retrieval workflows, and LLM integration.

### AutoGen

Used to prototype specialized reviewer agents and collaborative review workflows between security, performance, and bug-analysis agents.

---

## Repository Understanding

Repository context is incorporated into reviews using semantic indexing and retrieval.

### LlamaIndex

Used for:

- Repository indexing
- Multi-file context retrieval
- Document abstraction
- Context-aware repository analysis

This allows reviewer agents to understand relationships between files instead of evaluating code in isolation.

---

## Local and Cloud LLM Support

### Local Models

Powered by Ollama:

- Qwen2.5-Coder
- CodeLlama
- DeepSeek-Coder

### Cloud Models

Supported providers:

- Hugging Face Inference API
- OpenAI APIs

This hybrid architecture enables both private on-device inference and scalable cloud-hosted deployments.

---

## Hybrid Analysis Pipeline

The review process combines deterministic analysis with LLM reasoning.

### Stage 1: Static Analysis

- AST analysis
- Complexity metrics
- Rule-based validation

### Stage 2: Semantic Retrieval

- Embedding generation
- Vector similarity search
- Knowledge retrieval

### Stage 3: Multi-Agent Review

- Specialized reviewer execution
- Context-aware prompting
- Structured findings generation

### Stage 4: Consensus Generation

- Result aggregation
- Deduplication
- Confidence calibration

---

## C++ Vector Retrieval Engine

To explore retrieval performance for RAG workflows, a lightweight C++ vector retrieval engine was implemented and benchmarked.

### Features

- Cosine similarity implementation
- Top-k retrieval
- Vector ranking
- Latency benchmarking

### Benchmark Results

| Metric | Value |
|----------|----------|
| Dataset Size | 5,000 embeddings |
| Embedding Dimension | 384 |
| Top-K Retrieval | 5 |
| Benchmark Runs | 100 |
| Average Retrieval Latency | 15.1 ms |

### Implementation

The engine benchmarks semantic retrieval workloads similar to those used in RAG-based code review systems and serves as a performance-focused prototype for high-throughput retrieval.

---

## Benchmarking and Evaluation

The platform includes an evaluation framework for measuring review quality.

### Metrics

- Precision
- Recall
- F1 Score
- Severity Accuracy
- Category Accuracy
- Review Coverage
- Time Savings

### Evaluation Process

AI-generated findings are compared against annotated ground-truth datasets to measure review effectiveness and consistency.

---

## VS Code Integration

### Review Capabilities

- Review active file
- Review selected code blocks
- Review Git diffs
- Auto-review on save

### Developer Experience

- Inline diagnostics
- Quick Fix suggestions
- Dashboard analytics
- Quality scoring
- Review history

---

## Technology Stack

### Languages

- Python
- C++
- TypeScript
- JavaScript

### AI & GenAI

- LangChain
- LangGraph
- LlamaIndex
- AutoGen
- OpenAI APIs
- Ollama
- Hugging Face

### Retrieval

- ChromaDB
- FAISS
- Embeddings
- Semantic Search
- RAG

### Backend

- FastAPI
- REST APIs

### Infrastructure

- Docker
- GitHub Actions
- CI/CD

### Developer Tooling

- VS Code Extension
- Diagnostics
- Quick Fix Actions
- Dashboard Analytics

---

## Future Enhancements

- Pull request review automation
- Multi-repository analysis
- Agent memory and long-term context
- Distributed retrieval infrastructure
- Enterprise-scale codebase support

---

## Author

Monik Patel

M.S. Computer Science Candidate  
The University of Texas at Arlington

Focused on GenAI agents, LLM applications, RAG systems, semantic retrieval, AI-powered developer tooling, and intelligent automation.