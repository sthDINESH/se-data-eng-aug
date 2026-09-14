# Vector DB
# - has vector
# - has metadata
# - could have similarity search built-in
# nearest neighbour retrieval

import faiss

from sentence_transformers import SentenceTransformer

import numpy as np

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# The sentences to encode
documents = [
    "Machine learning uses data",
    "Python is a programming language",
    "Football is a popular sport",
]

# 2. Calculate embeddings from documents by calling model.encode()
embeddings = model.encode(documents)

# Shape FAISS index
# Each document has been converted into a vector with many numbers.
# The second shape value tells us how many numbers are in each vector.
dimension = embeddings.shape[1]

# Create an empty FAISS search index.
# IndexFlatL2 compares vectors using L2 (Euclidean) distance.
# The index needs to know the vector length so it can compare vectors correctly.
index = faiss.IndexFlatL2(dimension)

# Add embeddings to index --> STore them as vectors
# Add all document vectors to the index so they can be searched.
# NumPy arrays are the numerical format expected by FAISS.
index.add(np.array(embeddings))

# Convert query to embedding
query = model.encode(["Artificial Intelligence"])

# Search for top 2 similar vectors
D, I = index.search(np.array(query), k=2)

print("D", D)
print("I", I)

# Print top 2 similar documents
print('Most similar documents:')
for i in I[0]:
    print(documents[i])

# RAG systems are an outer layer, Vector databases are usually a layer inside the RAG. Below is an example workflow:
# User Query
# Embedding Model
# Vector Search
# Relevant documents
# Documents added to prompt
# LLM response