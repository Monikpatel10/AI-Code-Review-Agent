#include "VectorStore.h"
#include "Similarity.h"
#include <algorithm>

void VectorStore::addChunk(const DocumentChunk& chunk) {
    chunks.push_back(chunk);
}

std::vector<SearchResult> VectorStore::searchTopK(const std::vector<float>& queryEmbedding, int k) const {
    std::vector<SearchResult> results;

    for (const auto& chunk : chunks) {
        float score = Similarity::cosineSimilarity(queryEmbedding, chunk.embedding);
        results.push_back({chunk.id, chunk.text, score});
    }

    std::sort(results.begin(), results.end(), [](const SearchResult& a, const SearchResult& b) {
        return a.score > b.score;
    });

    if (results.size() > static_cast<size_t>(k)) {
        results.resize(k);
    }

    return results;
}

size_t VectorStore::size() const {
    return chunks.size();
}
