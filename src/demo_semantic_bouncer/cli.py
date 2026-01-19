import logging
from pathlib import Path

import chromadb
import click
from langchain_core.documents.base import Document

from demo_semantic_bouncer.base import Collection
from demo_semantic_bouncer.chroma_collection import ChromaDB
from demo_semantic_bouncer.constants import PERSIST_DIRECTORY

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--collection", "collection_name", type=str, required=True)
@click.option("--file", "filepath", type=Path, required=True)
def create(collection_name: str, filepath: Path):
    # Load contents
    with open(filepath, "r") as f:
        content = f.read()
        collection = Collection.model_validate_json(content)

    # Create/load collection
    chroma = ChromaDB(collection_name=collection_name, persist_directory=PERSIST_DIRECTORY)
    chroma.clear_collection()

    # Add documents to collection
    documents = [Document(page_content=text.content, metadata={"route": text.route} | text.metadata) for text in collection.texts]
    chroma.add_documents(documents)
    logger.info(f"Collection {collection_name} created and populated with {len(collection.texts)} documents.")


@cli.command()
@click.option("--collection", "collection_name", type=str, required=True)
@click.option("--file", "filepath", type=Path, required=True)
def add(collection_name: str, filepath: Path):
    # Load contents
    with open(filepath, "r") as f:
        content = f.read()
        collection = Collection.model_validate_json(content)

    # Load collection
    chroma = ChromaDB(collection_name=collection_name, persist_directory=PERSIST_DIRECTORY)

    # Add documents to collection
    documents = [Document(page_content=text.content, metadata={"route": text.route} | text.metadata) for text in collection.texts]
    chroma.add_documents(documents)
    logger.info(f"Added {len(collection.texts)} documents to collection {collection_name}.")


@cli.command()
@click.option("--collection", "collection_name", type=str, required=True)
def delete(collection_name: str):
    # Create/load collection
    client = chromadb.PersistentClient(PERSIST_DIRECTORY)
    client.delete_collection(collection_name)


@cli.command()
def list():
    # Create/load collection
    client = chromadb.PersistentClient(PERSIST_DIRECTORY)
    collections = client.list_collections()
    print("Number of Collections:", len(collections))
    print()
    for collection in collections:
        print(collection.name)
        print("Size:", collection.count(), "Embeddings")
        print("Metadata:", collection.metadata)
        print()


@cli.command()
@click.option("--query", "query", type=str, required=True)
@click.option("--collection", "collection_name", type=str, required=True)
@click.option("--distance", "distance", type=float, required=False)
def bouncer(query: str, collection_name: str, distance: float = 0.2):
    chroma = ChromaDB(collection_name=collection_name, persist_directory=PERSIST_DIRECTORY)
    results = chroma.search(query=query)
    best_match, best_score = results[0]
    print(f"Best match ({best_score:.5f}): {best_match}")
    if best_score < distance:
        route = best_match.metadata["route"]
    else:
        route = "agent"
    print("Recommended Route:", route)


if __name__ == "__main__":
    cli()
