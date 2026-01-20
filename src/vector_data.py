from langchain_community.document_loaders import PyMuPDFLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
import yaml
from pathlib import Path
import os

src_path = Path(__file__).resolve().parent

from logger import logging

logging.info(f"Loading YAML file")
try:
    with open (src_path/"params.yaml", "r") as f:
        params = yaml.safe_load(f)
except Exception as e:
    logging.info(f"Failed to load YAML File: {e}")
    raise(e)

class PersistentVectorDB():
    def __init__(self, path_to_source_files: str,
                      chunk_size:int,
                      chunk_overlap:int,
                      embedding_model:str,
                      database_name:str,
                      path_to_components:str,
                      path_to_vector_db:str,
                      vectordb_name:str):
        self.path_to_source_files = path_to_source_files
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.database_name = database_name
        self.path_to_components = path_to_components
        self.path_to_vector_db = path_to_vector_db
        self.vectordb_name = vectordb_name
    
    def generate_vectordb(self)->Chroma:
        try:
            logging.info(f"setting up component path")
            components_path = os.path.join(src_path, self.path_to_components)
            vector_db_artifact_path = os.path.join(components_path, self.path_to_vector_db)

            logging.info(f"converting pdfs to documents")
            documents = PyPDFDirectoryLoader(path=self.path_to_source_files).load()
            
            logging.info(f"Splitting documents")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            splits = text_splitter.split_documents(documents)

            logging.info(f"Creating index")
            ollama_embedding = OllamaEmbeddings(model=self.embedding_model)
            vectorstore = Chroma.from_documents(documents=splits, embedding=ollama_embedding,
                                                persist_directory=vector_db_artifact_path)
            
            logging.info("setting up retriever")    
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            logging.info("Done creating Vector DB")
            return retriever
        except Exception as e:
            logging.info(f"{e}")

ret = PersistentVectorDB(path_to_source_files=src_path,
                      chunk_size=params["chunk_size"],
                      chunk_overlap=params["overlap"],
                      embedding_model=params["embedding_model"],
                      database_name="persistentdb",
                      path_to_components=params["path_to_components"],
                      path_to_vector_db=params["path_to_vectordb"],
                      vectordb_name=params["vectordb_name"])
retriever = ret.generate_vectordb()

    

# @tool
# def retrieve_and_answer(question: str) -> str:
#     """Search and return information about a topic from the document store."""
#     docs = retriever.invoke(question)
#     return "\n\n".join(doc.page_content for doc in docs)

# retriever_tool = retrieve_and_answer

# re = retriever_tool.invoke({"question":"Summarize Evaluating Anomaly Detectors for Simulated Highly\
# Imbalanced Industrial Classification Problems"})