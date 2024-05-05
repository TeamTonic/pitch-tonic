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
import tiktoken
from src.dataloader import DataProcessor, DocumentLoader
import os
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.ingestion.cache import IngestionCache
from pydantic import BaseModel
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser, MetadataAwareTextSplitter
from voyageai import Client as VoyageClient

voyage_client = VoyageClient(os.getenv("VOYAGE_API_KEY"))


class DocumentIndexer:
    """ Class for indexing documents using MongoDB Cosmos with unique database and collection names. """
    def __init__(self, mongo_uri: str, db_name: str = "tonic", collection_name: str = "tonic"):
        self.voyage_api_key = os.environ.get("VOYAGE_API_KEY")
        self.embedding_model_name = "voyage-large-2"
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongodb_client = pymongo.MongoClient(self.mongo_uri)
        self.mongo_vector_store = AzureCosmosDBMongoDBVectorSearch(mongodb_client=self.mongodb_client, db_name=self.db_name, collection_name=self.collection_name)
        # Settings
        self.embed_model = VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=self.voyage_api_key)
        # self.tokenizer = tiktoken.encoding_for_model(model_name=embedding_model_name).encode
        self.tokenizer = voyage_client.tokenize
        self.storage_context = StorageContext.from_defaults(vector_store=self.mongo_vector_store)
        # self.sentence_splitter = MetadataAwareTextSplitter(chunk_size=450, chunk_overlap=200, tokenizer=self.tokenizer )  
        self.sentence_splitter = SentenceSplitter(chunk_size=450, chunk_overlap=200, tokenizer=self.tokenizer )  
        self.embedding = VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=self.voyage_api_key)
        # Get Documents Raw Text As List
        self.documents = DocumentLoader().load_documents_from_folder("./add_your_files_here")

    def index_documents(self):

        # Load documents
        documents = self.documents
        for document in documents:
            # Split the document into manageable nodes (sentences or paragraphs)
            nodes = self.sentence_splitter.split_text(document.content)
            
            # Process each node (text chunk)
            for node_text in nodes:
                    content = node_text.from_node(metadata_mode=BaseModel.MetadataMode.ALL)
                    embedding = self.embed_model.get_text_embedding(content)
                    content.embedding = embedding 
                    self.mongo_vector_store.add(node=content)

        return self.mongo_vector_store # , nodes


class DocumentRetriever:

    """Class for retrieving documents using Azure CosmosDB MongoDB."""
    def __init__(self, connection_string, db_name, collection_name):
        self.connection_string = connection_string
        self.mongodb_client = pymongo.MongoClient(self.connection_string)
        self.vector_store = AzureCosmosDBMongoDBVectorSearch(
            mongodb_client=self.mongodb_client,
            db_name=db_name,
            collection_name=collection_name)
        self.chat_memory = []
        self.retriever = self.vector_store

    def search(self, query="What's so cool about Tonic-AI?", top_k=10):
        return self.vector_store.search(query, top_k)
    
