import os

import ir_datasets
import pyterrier as pt
import pyterrier_doc2query

if not pt.started():
    pt.init()
import json


METHOD = os.getenv("METHOD")

TOPIC_BASE = """<top>
<num>{id}</num>
<title>{title}</title>
</top>\n\n"""

def fix_ir_dataset_naming(dataset_name):
    return dataset_name.replace("/", "-")

def move_queries(dataset_name, index_query_path):
    dataset = ir_datasets.load(dataset_name)

    with open(f"{index_query_path}/queries.trec", "w") as f:
        for query in dataset.queries_iter():
            f.write(TOPIC_BASE.format(id=query.query_id, title=query.text))
    print("Queries moved")


def load_subcollection_patch_dict():
    with open("tripclick-subcollections.json", "r") as f:
        subcollection_patch_dict = json.load(f)
    return subcollection_patch_dict


def gen_docs(dataset_name, subcollection):
    subcollection_patch_dict = load_subcollection_patch_dict()

    dataset = ir_datasets.load(dataset_name)

    for doc in dataset.docs_iter():
        item_subcollection = subcollection_patch_dict.get(doc.doc_id)
        if int(item_subcollection[1]) > int(subcollection[1]):
            print(f"Skipping {doc.doc_id}")
            continue

        yield {"docno": doc.doc_id, "text": doc.default_text()}


def index(dataset_name, index_document_path, index_query_path, batch_size, num_samples):
    dataset_name, subcollection = dataset_name.split("-")
    move_queries(dataset_name, index_query_path)
    
    doc2query = pyterrier_doc2query.Doc2Query(batch_size=batch_size, append=True, num_samples=num_samples, verbose=True, fast_tokenizer=True)

    indexer = pt.index.IterDictIndexer(
        index_path=index_document_path,
        meta={"docno": 26, "text": 100000},
        meta_tags={"text": "ELSE"},
        verbose=True,
        )
    
    pipeline = doc2query >> indexer

    indexref = pipeline.index(gen_docs(dataset_name, subcollection))
    
    index = pt.IndexFactory.of(indexref)
    print("Indexing done\n_________________________________")
    print(index.getCollectionStatistics().toString())