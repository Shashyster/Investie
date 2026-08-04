from pydantic import BaseModel

class CompanyCreate(BaseModel):
    ticker: str
    name: str
    sector: str | None = None 