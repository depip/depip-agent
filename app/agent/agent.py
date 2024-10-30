from depip_agent.app.llm_model.bedrock_llm import BedrockLLM
from depip_agent.app.embedding_model.bedrock_embedding import BedrockEmbedding
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
            "Searches and returns knowledge from the programmable ip license or story protocol",
        )

        self.agent_executor = create_react_agent(llm_model.llm, tools=[tool], checkpointer=memory,
                                                 state_modifier=SystemMessage("Your name always is Depip. I provided knowledge for you about story protocol and programmable ip license. Help human answer their questions"))

    def invoke(self, query: str, session_id: str):
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        response = self.agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config)
        return response['messages'][-1].content


        
