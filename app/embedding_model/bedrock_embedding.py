import os,time
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from depip_agent.app.utils.boto3_client import Boto3Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore, VectorStoreRetriever
from langchain_community.vectorstores import FAISS
class BedrockEmbedding:
    def __init__(self) -> None:
        boto3Client = Boto3Client()
        self.embedding_model = BedrockEmbeddings(client = boto3Client.client, model_id='cohere.embed-english-v3')

    def createEmbeddingPDF(self):
        print('create embedding PDF')
        start_time = time.time()
        # load pdf
        pdf_loader = PyMuPDFLoader('app/knowledge/story_knowledge.pdf')
        docs = pdf_loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits, embedding=self.embedding_model
        )

        self.retriever = vectorstore.as_retriever()
        print("--- %s seconds to create embedding ---" % (time.time() - start_time))

    def loadVectorStore(self):
        print('load vector store')
        start_time = time.time()
        faiss_index_path = "app/knowledge/faiss_index"
        loaded_vectorstore = FAISS.load_local(folder_path=faiss_index_path, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
        self.retriever = loaded_vectorstore.as_retriever()
        print("--- %s seconds to load vector store ---" % (time.time() - start_time))