cmake_minimum_required(VERSION 3.10)
project(VectorSearchRAG)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(vector_search
    src/main.cpp
    src/VectorStore.cpp
    src/Similarity.cpp
)
