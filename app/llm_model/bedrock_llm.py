from langchain_aws import ChatBedrock
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from utils.boto3_client import Boto3Client
from langchain_core.vectorstores import VectorStoreRetriever
import os
from dotenv import load_dotenv
load_dotenv()

class BedrockLLM:
    def __init__(self, retriever: VectorStoreRetriever) -> None:
        # boto3Client = Boto3Client()

        # self.llm = ChatBedrock(client=boto3Client.client, model_id='anthropic.claude-3-sonnet-20240229-v1:0')
        self.llm = ChatVertexAI(model_name='models/gemini-1.5-pro')
        # self.llm = ChatGoogleGenerativeAI(google_api_key=os.getenv('GOOGLE_API_KEY'), model='models/gemini-1.5-pro')