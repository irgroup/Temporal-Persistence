import os
from argparse import ArgumentParser

from indexer import fix_ir_dataset_naming, index

METHOD = os.getenv("METHOD")
TYPE = os.getenv("TYPE")


def get_artefact_path(artefact_name):
    artefact_type = TYPE
    if artefact_type == "index":
        return f"/data/index/index-{artefact_name}-{METHOD}"
    elif artefact_type == "run":
        return f"/data/runs/"
    elif artefact_type == "model":
        return f"/data/models/model-{artefact_name}-{METHOD}"
    else:
        raise ValueError(f"Artefact type `{artefact_type}` not supported!")


def setup_index_dir(dataset_name):
    index_path = get_artefact_path(dataset_name)
    print(f"Setting up index directory at {index_path}")
    os.makedirs(f"{index_path}/documents")
    os.makedirs(f"{index_path}/queries")


def main():
    parser = ArgumentParser(description="")
    parser.add_argument(
        "--dataset_name",
        help="Name or path to the dataset to be processed",
        required=True,
    )
    parser.add_argument(
        "--model_name", help="Name or path to the model", default="intfloat/e5-base"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="Batch size for encoding",
    )
    parser.add_argument("--save", type=int, help="Save every x batches", default=1000)

    args = parser.parse_args()

    dataset_name = fix_ir_dataset_naming(args.dataset_name)
    setup_index_dir(dataset_name)

    index_document_path = get_artefact_path(dataset_name) + "/documents"
    index_query_path = get_artefact_path(dataset_name) + "/queries"

    index(
        args.dataset_name,
        index_document_path,
        index_query_path,
        args.model_name,
        args.batch_size,
        args.save,
    )


if __name__ == "__main__":
    main()