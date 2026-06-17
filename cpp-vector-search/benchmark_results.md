# C++ Vector Search Benchmark

This module benchmarks a lightweight C++ vector search implementation for RAG-based code retrieval workflows.

## Benchmark Configuration

| Metric | Value |
|---|---:|
| Dataset Size | 5,000 embeddings |
| Embedding Dimension | 384 |
| Top-K | 5 |
| Runs | 100 |
| Average Retrieval Latency | 15.113 ms |

## Sample Output

```text
C++ Vector Search Benchmark
Dataset Size: 5000 embeddings
Embedding Dimension: 384
Top-K: 5
Runs: 100
Average Retrieval Latency: 15.113 ms

Top Results:
chunk_318 | score=0.800441 | Sample code chunk 318
chunk_940 | score=0.798427 | Sample code chunk 940
chunk_2141 | score=0.794992 | Sample code chunk 2141
chunk_4421 | score=0.793799 | Sample code chunk 4421
chunk_2507 | score=0.793611 | Sample code chunk 2507

## Implementation Details

- Implements cosine similarity from scratch in C++
- Supports top-k semantic retrieval over embedding vectors
- Uses 384-dimensional vectors to mirror common embedding model output sizes
- Benchmarks average retrieval latency across 100 runs
- Intended as a performance-focused prototype for RAG-based AI code review retrieval