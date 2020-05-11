import itertools
import json
import nltk
import pickle
import tqdm

TOKEN_BASED_ANNOTATIONS = "token_based/annotations.pkl"
VECTOR_BASED_ANNOTATIONS = "vector_based/annotations.pkl"


def load_annotations(file_path):
    return pickle.load(open(file_path, "rb"))


def num_tokens(sent):
    return len(nltk.word_tokenize(sent))


# Top 5 facts from each array then interleaved.
def merge(facts1, facts2):
    facts = facts1[:5] + facts2[:5]
    facts1 = facts1[5:]
    facts2 = facts2[5:]

    # Interleave the remaining facts.
    rem_facts = itertools.chain(*itertools.zip_longest(facts1, facts2))
    rem_facts = list(filter(lambda x: x is not None, rem_facts))
    assert(len(rem_facts) == len(facts1) + len(facts2))
    assert(len(rem_facts) <= 70 * 2)
    del facts1
    del facts2
    num_total_tokens = sum([num_tokens(fact) for fact in facts])
    for fact in rem_facts:
        if num_total_tokens >= 512:
            break
        facts.append(fact)
        num_total_tokens += num_tokens(fact)
    assert(num_total_tokens == sum([num_tokens(fact) for fact in facts]))

    # Remove duplicate facts, keep order.
    unique_facts = []
    for fact in facts:
        if fact not in unique_facts:
            unique_facts.append(fact)
    context = " . ".join(unique_facts)
    return context


def main():
    token_based = load_annotations(TOKEN_BASED_ANNOTATIONS)
    vector_based = load_annotations(VECTOR_BASED_ANNOTATIONS)
    assert(len(token_based) == len(vector_based))
    assert(isinstance(vector_based, dict))
    assert(isinstance(token_based, dict))

    out = {}
    for sent in tqdm.tqdm(vector_based):
        vector_facts = vector_based[sent]
        token_facts = token_based[sent]
        assert(isinstance(vector_facts, list))
        assert(isinstance(token_facts, list))
        out[sent] = {
                "context": merge(token_facts, vector_facts),
                "token_based": token_facts,
                "vector_based": vector_facts
        }
        assert(len(out[sent]["vector_based"]) == 75)
    # pickle.dump(out, open("annotations.pkl", "wb"))
    with open("annotatons.json", "wt") as g:
        g.write(json.dumps(out, indent=4, sort_keys=False))
        g.flush()


if __name__ == "__main__":
    nltk.download('punkt')   # for tokenization
    main()
