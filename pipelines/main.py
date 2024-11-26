from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import os
import time

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama

class Pipeline:
    def __init__(self):
        self.type = "pipe"
        self.id = "langchain_pipe"
        self.name = "LangChain Pipe"
        self.last_emit_time = 0
        pass
    
    async def on_startup(self):
        # This function is called when the server is started.
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass
    
    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]: