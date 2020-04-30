import data_mine as dm

from data_mine.nlp.CSQA import CSQAType


def main():
    print("Train examples:")
    print(dm.CSQA(CSQAType.TRAIN))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Dev examples:")
    print(dm.CSQA(CSQAType.DEV))  # Displays a Pandas DataFrame.
    print("\n\n")

    print("Test examples:")
    print(dm.CSQA(CSQAType.TEST))  # Displays a Pandas DataFrame.


if __name__ == "__main__":
    main()
