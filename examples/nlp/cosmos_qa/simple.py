import data_mine as dm

from data_mine.nlp.cosmos_qa import CosmosQAType


def main():
    df = dm.COSMOS_QA(CosmosQAType.TRAIN)
    print(df)
    print("\n")

    df = df.sample(n=1)
    row = next(df.iterrows())[1]
    print("Question: ", row.question, "\n")
    print("Context: ", row.context, "\n")
    for i, answer in enumerate(row.answers):
        print("{}) {}".format(chr(ord('A') + i), answer))
    print("\nCorrect answer: {}".format(row.correct))


if __name__ == "__main__":
    main()
