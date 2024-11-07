from langchain_aws import ChatBedrock
from utils.boto3_client import Boto3Client
from langchain_core.vectorstores import VectorStoreRetriever
class BedrockLLM:
    def __init__(self, retriever: VectorStoreRetriever) -> None:
        boto3Client = Boto3Client()

        self.llm = ChatBedrock(client=boto3Client.client, model_id='anthropic.claude-3-sonnet-20240229-v1:0')