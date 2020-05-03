import os
import pickle

from annoy import AnnoyIndex
from data_mine.nlp.allen_ai_obqa import OBQAFacts


def load_embeddings():
    return pickle.load(open("embeddings.pkl", "rb"))


def get_embeddings_dim(embeddings):
    dim = None
    for embedding in embeddings.values():
        new_dim = len(embedding)
        if dim is None:
            dim = new_dim
        else:
            assert(new_dim == dim)  # All embeddings have the same dimention.
    return dim


def main():
    if not os.path.isfile("embeddings.pkl"):
        raise RuntimeError("embeddings.pkl is required but not found.")
    embeddings = load_embeddings()
    print("Found {} embeddings.".format(len(embeddings)))

    # Annoy uses Euclidean distance of normalized vectors for its angular
    # distance, which for two vectors u,v is equal to sqrt(2(1-cos(u,v))).
    index = AnnoyIndex(get_embeddings_dim(embeddings), "angular")
    sentence_ids = {}
    for idx, fact in enumerate(OBQAFacts()):
        index.add_item(idx, embeddings[fact])
        sentence_ids[idx] = fact
    index.build(100)  # N trees TODO(sebisebi): test
    index.save('index.ann')
    pickle.dump(sentence_ids, open("sentence_ids.pkl", "wb"))
    print("Index saved to index.ann")
    print("Sentence IDs saved to sentence_ids.pkl")


if __name__ == "__main__":
    main()
