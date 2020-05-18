import data_mine as dm

from data_mine.nlp.hotpot_qa import HotpotQAType


def main():
    df = dm.HOTPOT_QA(HotpotQAType.DEV_DISTRACTOR)
    print(df)
    print("\n")

    df = df.sample(n=1)
    row = next(df.iterrows())[1]
    gold_paragraphs = row.gold_paragraphs
    print("Question: ", row.question)
    print("Answer: ", row.answer, "\n")
    for i, paragraph in enumerate(gold_paragraphs):
        print("Paragraph {}) {}\n".format(chr(ord('A') + i), paragraph))


if __name__ == "__main__":
    main()
