# ./src/dataloader.py

import os
from typing import Any, Optional, List
import llama_index
from llama_index.readers.file.docs import DocxReader, HWPReader, PDFReader
from llama_index.readers.file.epub import EpubReader
from llama_index.readers.file.flat import FlatReader
from llama_index.readers.file.html import HTMLTagReader
from llama_index.readers.file.image import ImageReader
# from llama_index.readers.file.image_caption import ImageCaptionReader
# from llama_index.readers.file.image_deplot import ImageTabularChartReader
# from llama_index.readers.file.image_vision_llm import ImageVisionLLMReader
# from llama_index.readers.file.ipynb import IPYNBReader
from llama_index.readers.file.markdown import MarkdownReader
from llama_index.readers.file.mbox import MboxReader
# from llama_index.readers.file.paged_csv import PagedCSVReader
# from llama_index.readers.file.pymu_pdf import PyMuPDFReader
from llama_index.readers.file.slides import PptxReader
from llama_index.readers.file.tabular import PandasCSVReader, CSVReader
# from llama_index.readers.file.unstructured import UnstructuredReader 
from llama_index.readers.file.xml import XMLReader
# from llama_index.readers.file.rtf import RTFReader
# from llama_index.readers.file import VideoAudioReader 
# from llama_index.readers.file import ImageVisionLLMReader # https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/image_vision_llm/base.py
# from llama_index.readers.file import SimpleDirectoryReader
# from llama_index.core.node_parser import SentenceSplitter

# import llama_parse
# from llama_parse import LlamaParse

# from langchain_community_core.documents.base import Document

import os


class DataProcessor:
    def __init__(self, source_file: str):
        self.source_file = source_file

    def load_data_from_source(self):
        """Loads data from the source file and returns the text as a list of paragraphs."""
        ext = os.path.splitext(self.source_file)[-1].lower()

        # Dictionary mapping for extension to appropriate reader class instances
        reader_map = {
            '.csv': CSVReader(),
            '.docx': DocxReader(),
            '.epub': EpubReader(),
            '.html': HTMLTagReader(),
            '.hwp': HWPReader(),
            '.ipynb': FlatReader(),  # Assuming IPYNB files are read by a FlatReader
            '.png': ImageReader(),
            '.jpg': ImageReader(),
            '.jpeg': ImageReader(),
            '.md': MarkdownReader(),
            '.mbox': MboxReader(),
            '.pdf': PDFReader(),
            '.pptx': PptxReader(),
            '.xml': XMLReader(),
            '.txt': FlatReader(),
        }

        reader = reader_map.get(ext)
        if reader is not None:
            return reader.load_data(self.source_file)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

class DocumentLoader:
    @staticmethod
    def load_documents_from_folder(folder_path: str):
        """Loads all supported documents from files within a specified folder and returns them as a list of content."""
        documents = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                try:
                    processor = DataProcessor(source_file=full_path)
                    doc_content = processor.load_data_from_source()
                    documents.append(doc_content)
                    print(f"Loaded document from '{filename}'")
                except Exception as e:
                    print(f"Failed to load document from '{filename}'. Error: {e}")
        return documents
