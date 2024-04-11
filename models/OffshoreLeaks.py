from pydantic import BaseModel

class OffshoreLeaks(BaseModel):
    entity: str
    jurisdiction: str
    linked_to: str
    data_from: str
