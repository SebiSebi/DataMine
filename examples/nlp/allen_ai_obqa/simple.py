import data_mine as dm

from data_mine.nlp.allen_ai_obqa import OBQAType


def main():
    print("Train examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.TRAIN))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Dev examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.DEV))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Test examples:")
    print(dm.ALLEN_AI_OBQA(OBQAType.TEST))  # Displays a Pandas DataFrame.


if __name__ == "__main__":
    main()
