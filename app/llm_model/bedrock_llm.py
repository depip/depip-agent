from langchain_core.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from depip_agent.app.utils.boto3_client import Boto3Client
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.vectorstores import VectorStoreRetriever
class BedrockLLM:

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    

    def __init__(self, retriever: VectorStoreRetriever) -> None:
        boto3Client = Boto3Client()

        self.llm = ChatBedrock(client=boto3Client.client, model_id='anthropic.claude-3-sonnet-20240229-v1:0')
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(self.llm, retriever, contextualize_q_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

