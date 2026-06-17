#ifndef VECTOR_STORE_H
#define VECTOR_STORE_H

#include <string>
#include <vector>

struct DocumentChunk {
    std::string id;
    std::string text;
    std::vector<float> embedding;
};

struct SearchResult {
    std::string id;
    std::string text;
    float score;
};

class VectorStore {
private:
    std::vector<DocumentChunk> chunks;

public:
    void addChunk(const DocumentChunk& chunk);
    std::vector<SearchResult> searchTopK(const std::vector<float>& queryEmbedding, int k) const;
    size_t size() const;
};

#endif
