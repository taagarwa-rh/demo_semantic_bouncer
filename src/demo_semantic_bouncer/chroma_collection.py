import logging

from langchain_chroma import Chroma
from langchain_core.documents.base import Document
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)


class ChromaDB:
    def __init__(self, collection_name, persist_directory, embedding_model: str = "ibm-granite/granite-embedding-125m-english"):
        """Initialize ChromaDB and create/load the collection."""
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Get embedding function
        self.embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)

        # Create/Load Chroma collection
        self.chroma = Chroma(
            persist_directory=self.persist_directory, collection_name=self.collection_name, embedding_function=self.embedding_function
        )

    def delete_collection(self):
        """Delete the collection."""
        self.chroma.delete_collection()

    def clear_collection(self):
        """Clear and recreate the collection."""
        self.delete_collection()
        self.chroma = Chroma(
            persist_directory=self.persist_directory, collection_name=self.collection_name, embedding_function=self.embedding_function
        )

    def add_documents(self, texts: list[Document]):
        """Add a document to the collection."""
        self.chroma.add_documents(texts)

    def search(self, query: str):
        """Search the collection for documents."""
        results = self.chroma.similarity_search_with_score(query, k=3)
        return results
