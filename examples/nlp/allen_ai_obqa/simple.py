import data_mine as dm
import random

from data_mine.nlp.allen_ai_obqa import OBQAFacts, OBQAType


def main():
    print("Train examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.TRAIN))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Dev examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.DEV))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Test examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.TEST))  # Displays a Pandas DataFrame.
    print("\n\n")

    facts = list(OBQAFacts())
    assert(len(facts) == 1326)  # There are 1326 core facts in total.
    print("Some random facts from OpenBookQA:")
    random.shuffle(facts)
    for fact in facts[:10]:
        print("    * {}".format(fact))
    print("\n\n")

    print("Train examples with retrieved facts:")
    print(dm.ALLEN_AI_OBQA(OBQAType.TRAIN, True))
    print("\n\n")


if __name__ == "__main__":
    main()
