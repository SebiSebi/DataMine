import data_mine as dm
import lucene
import os
import pandas as pd

from data_mine.nlp.allen_ai_obqa import OBQAType
from java.nio.file import Paths
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory


def get_random_question():
    df = pd.concat(map(dm.ALLEN_AI_OBQA, list(OBQAType))).sample(n=1)
    row = next(df.iterrows())[1]
    return row.question


def search(query_string, analyzer, searcher):
    query = QueryParser("contents", analyzer).parse(query_string)
    hits = searcher.search(query, 10).scoreDocs
    print("\nQuery: {}\n".format(query_string))
    for i, score_doc in enumerate(hits):
        fact = searcher.doc(score_doc.doc).get("contents")
        score = score_doc.score
        print("{}) {} (score: {})".format(i + 1, fact, score))


def main():
    store_dir = "lucene_index"
    if not os.path.isdir(store_dir):
        raise RuntimeError("Cannot find Lucene index at: {}".format(store_dir))
    store = SimpleFSDirectory(Paths.get(store_dir))
    searcher = IndexSearcher(DirectoryReader.open(store))
    analyzer = EnglishAnalyzer()

    # query_string = "House is a simple fact about science reaction"
    query_string = get_random_question()
    search(query_string, analyzer, searcher)
    del searcher


if __name__ == "__main__":
    lucene.initVM()
    print("Lucene version: {}".format(lucene.VERSION))
    main()
