#ifndef SIMILARITY_H
#define SIMILARITY_H

#include <vector>

class Similarity {
public:
    static float cosineSimilarity(const std::vector<float>& a, const std::vector<float>& b);
};

#endif
