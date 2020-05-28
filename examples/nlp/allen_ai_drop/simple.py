import data_mine as dm

from data_mine.nlp.allen_ai_drop import DROPType, DROP2MC


def main():
    df = dm.ALLEN_AI_DROP(DROPType.DEV)
    print(df)

    df = DROP2MC(df)
    print(df)


if __name__ == "__main__":
    main()
