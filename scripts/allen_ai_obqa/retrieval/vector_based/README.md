# Retrieve facts for OpenBookQA

Steps to run:

1. Run `encode_all.py` - it creates a file (`embeddings.pkl`) with a dictionary
from sentences (facts and questions in OpenBookQA) to their computed embeddings.

2. Run `create_index.py` - it creates two files: an `Annoy` index (`index.ann`)
and another file with a map from sentence IDs (used in the index) to the actual
sentences (`sentence_ids.pkl`). `Annoy` requires that items attached to vectors
are integers. When searching the index, the attached integers are returned. We
need the `ID -> sentence` map to get the original sentences.
