from pydantic import BaseModel, Field
from typing import List

class Parameters(BaseModel):
    service_host : str
    service_port : int
    urls_for_searching : List[str]
    bss_bert_url : str
    bss_pubs : List[int]
    timeout_seconds : float
    max_text_len: int

class SearchData(BaseModel):
    """"""
    pubid: int = Field(title="Пабайди, в котором будет поиск дублей")
    text: str = Field(title="вопрос для поиска")
