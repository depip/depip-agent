from typing import Annotated
from pydantic import BaseModel
from fastapi import Form, UploadFile, File
from enum import Enum

class DestinationLanguage(str, Enum):
    English = 'en'
    Vietnamese = 'vi'

class TranslateMangaInputDTO(BaseModel):
    image: Annotated[bytes, File()]
    destination_lang: Annotated[DestinationLanguage, Form()]