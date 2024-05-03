# src/upsert_retrieve.py

import pymongo
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
# from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.azurecosmosmongo import AzureCosmosDBMongoDBVectorSearch # https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-azurecosmosmongo/llama_index/vector_stores/azurecosmosmongo/base.py
from llama_index.storage.docstore.mongodb import MongoDocumentStore # https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/storage/docstore/llama-index-storage-docstore-mongodb/llama_index/storage/docstore/mongodb/base.py
from llama_index.storage.kvstore.mongodb import MongoDBKVStore # https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/storage/kvstore/llama-index-storage-kvstore-mongodb/llama_index/storage/kvstore/mongodb/base.py
from llama_index.embeddings.voyageai import VoyageEmbedding
from src.utilities import generate_unique_name
from global_variables import embedding_model_name
# from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from src.dataloader import DataProcessor, DocumentLoader
import os
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.ingestion.cache import IngestionCache
from pydantic import BaseModel
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser


class DocumentIndexer:
    """ Class for indexing documents using MongoDB Cosmos with unique database and collection names. """
    def __init__(self, transformations, mongo_uri: str, db_name: str = "tonic", collection_name: str = "tonic"):
        self.mongo_uri = mongo_uri
        # Using unique names
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongodb_client = pymongo.MongoClient(self.mongo_uri)
        # Create KV Store Using Client
        self.voyage_api_key = os.environ.get("VOYAGE_API_KEY")
        self.mongo_docstore = MongoDocumentStore(self.mongodb_client)
        # Return Client
        self.embedding_model_name = os.environ.get("")
        self.mongodb_kvstore = MongoDBKVStore(self.mongodb_client).from_uri(uri = self.mongo_uri, db_name = self.db_name)
        self.mongo_vectorstore = AzureCosmosDBMongoDBVectorSearch(mongodb_client=self.mongodb_client, db_name=self.db_name, collection_name=self.collection_name)
        # Settings 
        self.embed_model = VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=self.voyage_api_key)
        self.storage_context = StorageContext.from_defaults(index_store=self.mongodb_kvstore, vector_store=self.mongo_vectorstore, docstore=self.mongo_docstore)
        self.transformations = [
        SentenceSplitter(chunk_size=450, chunk_overlap=200), MarkdownNodeParser() , VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=self.voyage_api_key) 
        ]
        # Get Documents Raw Text As List
        self.documents = DocumentLoader().load_documents_from_folder("./add_your_files_here")

    def index_documents(self):

        # Load documents
        documents = self.documents
        
        ingest = IngestionPipeline(
                    transformations=self.transformations,
                    cache=IngestionCache(
                        cache= self.mongodb_kvstore
                        )
                    )

        # Run ingestion pipeline to process and transform documents into nodes
        nodes = ingest.run(documents=documents)
        
        # Embed nodes and store them
        for node in nodes:
            if isinstance(node):
                content = node.from_node(metadata_mode=BaseModel.MetadataMode.ALL)
                embedding = self.embed_model.get_text_embedding(content)
                content.embedding = embedding  # Set the embedding
                
                # Store each node with its new embedding using MongoDB
                self.mongodb_kvstore.add(node=content)  

        return self.mongodb_kvstore , nodes
class DocumentRetriever:
    """Class for retrieving documents using Azure CosmosDB MongoDB."""
    def __init__(self, connection_string, db_name, collection_name):
        self.connection_string = connection_string
        self.mongodb_client = pymongo.MongoClient(self.connection_string)
        self.vector_store = AzureCosmosDBMongoDBVectorSearch(
            mongodb_client=self.mongodb_client,
            db_name=db_name,
            collection_name=collection_name)
    
    def search(self, query="What's so cool about Tonic-AI?", top_k=10):
        return self.vector_store.search(query, top_k)