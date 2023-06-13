from pydantic import BaseModel, Field, List


class Parameters(BaseModel):
    service_host : int
    service_port : int
    urls_for_searching : List[str]
    bss_bert_url : str
    bss_pubs : List[int]
    timeout_seconds : float

class SearchData(BaseModel):
    """"""
    pubid: int = Field(title="Пабайди, в котором будет поиск дублей")
    text: str = Field(title="вопрос для поиска")
