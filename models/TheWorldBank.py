from pydantic import BaseModel
class TheWorldBank(BaseModel):
    first_name: str
    address: str
    country: str
    from_date: str
    to_date: str
    grounds: str
