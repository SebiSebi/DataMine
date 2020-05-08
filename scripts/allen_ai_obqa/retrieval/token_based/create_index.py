import data_mine as dm
import lucene
import tqdm

from data_mine.nlp.allen_ai_obqa import OBQAFacts
from java.nio.file import Paths
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory


def get_all_facts():
    sentences = list(OBQAFacts())
    return list(set(sentences))


def index_facts(facts, writer):
    for fact in tqdm.tqdm(facts, desc="Indexing facts"):
        doc = Document()
        doc.add(TextField("contents", fact, Field.Store.YES))
        writer.addDocument(doc)


def main():
    facts = get_all_facts()
    print("Preparing to index {} facts".format(len(facts)))
    
    store_dir = "lucene_index"
    store = SimpleFSDirectory(Paths.get(store_dir))
    analyzer = EnglishAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
    writer = IndexWriter(store, config)
    index_facts(facts, writer)
    writer.commit()
    writer.close()
    print("Lucene index created at: {}".format(store_dir))


if __name__ == "__main__":
    lucene.initVM()
    print("Lucene version: {}".format(lucene.VERSION))
    main()
