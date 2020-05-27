import data_mine as dm

from data_mine.nlp.allen_ai_arc import ARCType


def main():
    df = dm.ALLEN_AI_ARC(ARCType.TEST_EASY)
    print(df)  # Shows something similar to the example below.


if __name__ == "__main__":
    main()
