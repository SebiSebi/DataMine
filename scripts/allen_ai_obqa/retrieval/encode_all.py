import pickle

from data_mine.nlp.allen_ai_obqa import OBQAFacts
from sentence_transformers import SentenceTransformer


def get_all_sentences():
    sentences = list(OBQAFacts())
    return sentences


def main():
    model = SentenceTransformer("roberta-large-nli-mean-tokens")
    sentences = get_all_sentences()
    sentence_embeddings = model.encode(sentences, show_progress_bar=True)
    assert(len(sentence_embeddings) == len(sentences))
    data = {}
    for sentence, embedding in zip(sentences, sentence_embeddings):
        data[sentence] = embedding
    pickle.dump(data, open("embeddings.pkl", "wb"))
    print("Embeddings written to embeddings.pkl")


if __name__ == "__main__":
    main()
