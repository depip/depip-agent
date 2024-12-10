from llm_model.bedrock_llm import BedrockLLM
from embedding_model.bedrock_embedding import BedrockEmbedding
from langgraph.prebuilt import create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
class Agent:
    def __init__(self, embedding_model: BedrockEmbedding, llm_model: BedrockLLM) -> None:
        # embedding_model = BedrockEmbedding()
        # llm_model = BedrockLLM(embedding_model.retriever)
        memory = MemorySaver()
        tool = create_retriever_tool(
            embedding_model.retriever,
            "programmable_ip_license",
            "Searches and returns knowledge, example codes from the programmable ip license or story protocol",
        )
        instruction = "You are Depip, a friendly and knowledgeable AI assistant specializing in Story Protocol and programmable IP licenses. Your goal is to help users understand and answer their questions about these topics using accurate and up-to-date knowledge retrieved from the embedding model. Always use the embedding model to search for relevant knowledge before answering. If the retrieved knowledge is insufficient or does not address the question, politely explain that you do not have enough information to provide an accurate answer. Stay focused on the topics of Story Protocol and programmable IP licenses. Do not provide information outside this scope, and avoid making up answers. Use clear, concise, and professional language to ensure users easily understand your responses."
        self.agent_executor = create_react_agent(llm_model.llm, tools=[tool], 
                                                 checkpointer=memory, state_modifier=instruction)

    def invoke(self, query: str, session_id: str):
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        response = self.agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config)
        return response['messages'][-1].content


        
