# .src/upsert_retrieve.py

import pymongo

from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.azurecosmosmongo import AzureCosmosDBMongoDBVectorSearch
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from src.dataloader import DataProcessor, DocumentLoader
import os

class DocumentIndexer:
    """Class for indexing documents using MongoDB Atlas."""
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.mongodb_client = pymongo.MongoClient(self.mongo_uri)
        self.store = MongoDBAtlasVectorSearch(self.mongodb_client)
        self.storage_context = StorageContext.from_defaults(vector_store=self.store)
        
    def index_documents(self, document_loader=DocumentLoader()):
        index = VectorStoreIndex.from_documents(document_loader, storage_context=self.storage_context)
        return index

class DocumentRetriever:
    """Class for retrieving documents using Azure CosmosDB MongoDB."""
    def __init__(self, connection_string, db_name, collection_name):
        self.connection_string = connection_string
        self.mongodb_client = pymongo.MongoClient(self.connection_string)
        self.vector_store = AzureCosmosDBMongoDBVectorSearch(
            mongodb_client=self.mongodb_client,
            db_name=db_name,
            collection_name=collection_name)
    
    def search(self, query, top_k=10):
        return self.vector_store.search(query, top_k)

# Usage example for both classes:

# # Assuming a setup for DocumentIndexer
# mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://<username>:<password>@<host>?retryWrites=true&w=majority")
# indexer = DocumentIndexer(mongo_uri)

# # Assuming you have a document loader set up
# document_loader = DocumentLoader()  # Assuming this loader is already configured
# index = indexer.index_documents(document_loader)

# # Assuming a setup for DocumentRetriever
# azure_conn_string = os.getenv("AZURE_CONNECTION_STRING", "YOUR_AZURE_COSMOSDB_MONGODB_URI")
# retriever = DocumentRetriever(azure_conn_string, "demo_vectordb", "paul_graham_essay")

# # Use a sample query vector to search
# sample_query_vector = [0.1, 0.2, 0.3]  # This needs to be replaced with an actual data vector
# search_results = retriever.search(sample_query_vector, top_k=5)
# print(search_results)

# #Vector Store
# # mongo_uri = os.environ["MONGO_URI"]
# mongo_uri = (
#     "mongodb+srv://<username>:<password>@<host>?retryWrites=true&w=majority"
# )

# mongodb_client = pymongo.MongoClient(mongo_uri)
# store = MongoDBAtlasVectorSearch(mongodb_client)
# storage_context = StorageContext.from_defaults(vector_store=store)
# docs = DocumentLoader()
# #     input_files=["./data/10k/uber_2021.pdf"]
# # ).load_data()
# index = VectorStoreIndex.from_documents(
#      docs, storage_context=storage_context
# # )


# Vector Search
# Set up the connection string with your Azure CosmosDB MongoDB URI
connection_string = "YOUR_AZURE_COSMOSDB_MONGODB_URI"
mongodb_client = pymongo.MongoClient(connection_string)

# Create an instance of AzureCosmosDBMongoDBVectorSearch
vector_store = AzureCosmosDBMongoDBVectorSearch(
    mongodb_client=mongodb_client,
    db_name="demo_vectordb",
    collection_name="paul_graham_essay",
)