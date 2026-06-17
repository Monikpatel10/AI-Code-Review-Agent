#include "VectorStore.h"
#include <chrono>
#include <iostream>
#include <random>
#include <vector>
#include <string>

std::vector<float> generateRandomEmbedding(int dimension) {
    static std::mt19937 generator(42);
    static std::uniform_real_distribution<float> distribution(0.0f, 1.0f);

    std::vector<float> embedding;
    embedding.reserve(dimension);

    for (int i = 0; i < dimension; ++i) {
        embedding.push_back(distribution(generator));
    }

    return embedding;
}

int main() {
    const int datasetSize = 5000;
    const int embeddingDimension = 384;
    const int topK = 5;
    const int runs = 100;

    VectorStore store;

    for (int i = 0; i < datasetSize; ++i) {
        DocumentChunk chunk;
        chunk.id = "chunk_" + std::to_string(i);
        chunk.text = "Sample code chunk " + std::to_string(i);
        chunk.embedding = generateRandomEmbedding(embeddingDimension);
        store.addChunk(chunk);
    }

    std::vector<float> queryEmbedding = generateRandomEmbedding(embeddingDimension);

    double totalMs = 0.0;
    std::vector<SearchResult> finalResults;

    for (int i = 0; i < runs; ++i) {
        auto start = std::chrono::high_resolution_clock::now();
        finalResults = store.searchTopK(queryEmbedding, topK);
        auto end = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = end - start;
        totalMs += duration.count();
    }

    double avgLatency = totalMs / runs;

    std::cout << "C++ Vector Search Benchmark\n";
    std::cout << "Dataset Size: " << datasetSize << " embeddings\n";
    std::cout << "Embedding Dimension: " << embeddingDimension << "\n";
    std::cout << "Top-K: " << topK << "\n";
    std::cout << "Runs: " << runs << "\n";
    std::cout << "Average Retrieval Latency: " << avgLatency << " ms\n\n";

    std::cout << "Top Results:\n";
    for (const auto& result : finalResults) {
        std::cout << result.id << " | score=" << result.score << " | " << result.text << "\n";
    }

    return 0;
}
