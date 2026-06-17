# C++ Vector Search Module

This module provides a lightweight C++ vector search prototype for RAG-based AI code review workflows.

It implements cosine similarity, top-k retrieval, and latency benchmarking across synthetic code embeddings. The goal is to demonstrate the retrieval logic behind semantic code chunk search used in AI review pipelines.

## Features

- C++17 implementation
- Cosine similarity scoring
- Top-k vector retrieval
- 384-dimensional embedding simulation
- Benchmarking across 5,000 embeddings
- Average retrieval latency measurement

## Build and Run

```bash
mkdir -p build
cd build
cmake ..
make
./vector_search