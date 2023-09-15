import os
import shutil
import pyterrier as pt
if not pt.started():
    pt.init()

METHOD = os.getenv("METHOD")

def get_dataset_subcollection(dataset):
    return dataset.split("-")[-2]


def get_querie_path(dataset):
    subcollection = get_dataset_subcollection(dataset)
    if subcollection == "LT":
        return  {"test": "/data/dataset/LongEval/test-collection/B-Long-September/English/Queries/test09.trec"}
    elif subcollection == "ST":
        return {"test": "/data/dataset/LongEval/test-collection/A-Short-July/English/Queries/test07.trec"}
    elif subcollection == "WT":
        return {
            "train": "/data/dataset/LongEval/publish/English/Queries/train.trec", 
            "test": "/data/dataset/LongEval/publish/English/Queries/heldout.trec"
            }


def get_documents_path(dataset):
    subcollection = get_dataset_subcollection(dataset)
    if subcollection == "LT":
        return "/data/dataset/LongEval/test-collection/B-Long-September/English/Documents/Trec/"
    elif subcollection == "ST":
        return "/data/dataset/LongEval/test-collection/A-Short-July/English/Documents/Trec/"
    elif subcollection == "WT":
        return "/data/dataset/LongEval/publish/English/Documents/Trec/"


def move_queries(dataset, index_query_path):
    querie_paths = get_querie_path(dataset)
    for key, path in querie_paths.items():
        shutil.copy(path, f"{index_query_path}/{key}.trec")
    

def index(dataset, index_document_path, index_query_path):
    move_queries(dataset, index_query_path)

    indexer = pt.TRECCollectionIndexer(
        index_path=index_document_path,
        meta={"docno": 26, "text": 100000},
        meta_tags={"text": "ELSE"},
        blocks=True,
        verbose=True,
    )
    documents_path = get_documents_path(dataset)
    documents = [os.path.join(documents_path, path) for path in os.listdir(documents_path)]
    indexref = indexer.index(documents)

    index = pt.IndexFactory.of(indexref)

    print("Indexing done\n_________________________________")
    print(index.getCollectionStatistics().toString())
