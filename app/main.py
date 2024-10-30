from typing import Union

from fastapi import FastAPI

from depip_agent.app.agent.agent import Agent
from depip_agent.app.embedding_model.bedrock_embedding import BedrockEmbedding
from depip_agent.app.llm_model.bedrock_llm import BedrockLLM
from depip_agent.app.dto import invoke_input

embedding_model = BedrockEmbedding()
embedding_model.createEmbeddingPDF()
llm_model = BedrockLLM(embedding_model.retriever)
agent = Agent(embedding_model=embedding_model, llm_model=llm_model)

app = FastAPI()
@app.post("/invoke")
def invokeLLM(input: invoke_input.InvokeInputDTO):
    return agent.invoke(query=input.query, session_id=input.session_id)