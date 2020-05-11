# Extract facts for OpenBookQA

The `OpenBookQA` dataset comes packed with a "book" of 1326 core science facts.
We retrieve supporting facts for each question using two strategies:

1. Token based - Lucene TF-IDF matching;
2. Vector based - cosine distance of transformer-based embeddings.
