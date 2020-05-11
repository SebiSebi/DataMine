import data_mine as dm
import os
import pandas as pd
import pickle
import tqdm

from annoy import AnnoyIndex
from data_mine.nlp.allen_ai_obqa import OBQAType


def load_embeddings():
    return pickle.load(open("embeddings.pkl", "rb"))


def load_sentence_ids():
    return pickle.load(open("sentence_ids.pkl", "rb"))


def get_embeddings_dim(embeddings):
    dim = None
    for embedding in embeddings.values():
        new_dim = len(embedding)
        if dim is None:
            dim = new_dim
        else:
            assert(new_dim == dim)  # All embeddings have the same dimention.
    return dim


def get_similar_sentences(query):
    embeddings = load_embeddings()
    sentence_ids = load_sentence_ids()
    index = AnnoyIndex(get_embeddings_dim(embeddings), "angular")
    index.load("index.ann")
    print("Found {} items in the index.".format(index.get_n_items()))
    print("The index uses {} trees.".format(index.get_n_trees()))
    print("")
    closest, dists = index.get_nns_by_vector(embeddings[query], 10, include_distances=True)  # noqa: E501
    assert(len(closest) == len(dists))
    closest = map(lambda sid: sentence_ids[sid], closest)
    return zip(closest, dists)


def by_sentence(query):
    similar = get_similar_sentences(query)
    print("Query: `{}`".format(query))
    for i, (sentence, dist) in enumerate(similar):
        print("{}) {} ({})".format(i, sentence, dist))


def by_random_question():
    df = pd.concat(map(dm.ALLEN_AI_OBQA, list(OBQAType))).sample(n=1)
    row = next(df.iterrows())[1]
    print("Question: " + row.question + "\n")
    for idx, answer in zip(["A", "B", "C", "D"], row.answers):
        print("{}) {}".format(idx, answer))
    print("")
    similar = get_similar_sentences(row.question)
    print("Similar facts:")
    for i, (sentence, dist) in enumerate(similar):
        print("{}) {} ({})".format(i, sentence, dist))


def annotate_all_questions():
    embeddings = load_embeddings()
    sentence_ids = load_sentence_ids()
    index = AnnoyIndex(get_embeddings_dim(embeddings), "angular")
    index.load("index.ann")
    print("Found {} items in the index.".format(index.get_n_items()))
    print("The index uses {} trees.".format(index.get_n_trees()))
    print("")

    df = pd.concat(map(dm.ALLEN_AI_OBQA, list(OBQAType)))
    annotations = {}
    for _, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        for answer in row.answers:
            sent = row.question + " " + answer
            closest = index.get_nns_by_vector(embeddings[sent], 75)
            closest = list(map(lambda sid: sentence_ids[sid], closest))
            annotations[sent] = closest
    pickle.dump(annotations, open("annotations.pkl", "wb"))
    print("Annotations written to annotations.pkl")


def main():
    required_files = [
            "embeddings.pkl",
            "index.ann",
            "sentence_ids.pkl",
    ]
    for required_file in required_files:
        if not os.path.isfile(required_file):
            raise RuntimeError("{} is required but not found.".format(required_file))  # noqa: E501

    # by_sentence("Pasta may be cooked in water when")
    # by_sentence("what is the closest source of plasma to our planet?")
    # by_sentence("If an organism is existing then it is made up of")
    # by_random_question()
    annotate_all_questions()


if __name__ == "__main__":
    main()
