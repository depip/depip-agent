from fastapi import FastAPI, File, Form, UploadFile
from typing import Annotated
from manga.manga import Manga
from agent.agent import Agent
from embedding_model.bedrock_embedding import BedrockEmbedding
from llm_model.bedrock_llm import BedrockLLM
from dto import invoke_input, translate_manga
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
load_dotenv()

embedding_model = BedrockEmbedding()
# embedding_model.createEmbeddingPDF()
embedding_model.loadVectorStore()
llm_model = BedrockLLM(embedding_model.retriever)
agent = Agent(embedding_model=embedding_model, llm_model=llm_model)

manga = Manga()

app = FastAPI(root_path=os.getenv('FASTAPI_ROOT_PATH'))

@app.post("/invoke")
def invokeLLM(input: invoke_input.InvokeInputDTO):
    return agent.invoke(query=input.query, session_id=input.session_id)

@app.post("/translate-manga")
def translateImage(image: Annotated[UploadFile, File()],
                   destination_lang: Annotated[translate_manga.DestinationLanguage, Form()]):
    translated_file = manga.translate_image(image=image.file.read(),
                                            destination_lang=destination_lang)
    return StreamingResponse(
        content=translated_file,
        media_type=image.content_type
        # headers={"Content-Disposition": f"attachment; filename={image.filename}"}
    )

