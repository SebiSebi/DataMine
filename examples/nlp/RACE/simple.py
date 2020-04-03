import data_mine as dm

from data_mine.nlp.RACE import RACEType


def main():
    df = dm.RACE(RACEType.DEV_MIDDLE)
    print(df)


if __name__ == "__main__":
    main()
