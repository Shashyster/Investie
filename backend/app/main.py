from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.fmp_service import get_company_profile, get_income_statement, get_balance_sheet, get_cash_flow, get_full_dcf_valuation

from app.db.session import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Investie API is running"}

@app.post("/companies")
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    new_company = Company(
        ticker=company.ticker,
        name=company.name,
        sector=company.sector,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@app.get("/companies")
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

@app.get("/fmp/{ticker}")
def fetch_fmp_data(ticker: str):
    return get_company_profile(ticker)

@app.get("/fmp/{ticker}/income")
def fetch_income_statement(ticker: str, period: str = "annual", limit: int = 10):
    return get_income_statement(ticker, period, limit)

@app.get("/fmp/{ticker}/balance-sheet")
def fetch_balance_sheet(ticker: str):
    return get_balance_sheet(ticker)

@app.get("/fmp/{ticker}/cash-flow")
def fetch_cash_flow(ticker: str):
    return get_cash_flow(ticker)

@app.get("/fmp/{ticker}/get_full_dcf_valuation")
def fetch_full_dcf_valuation(ticker: str):
    return get_full_dcf_valuation(ticker)

@app.post("/companies/fetch/{ticker}")
def fetch_and_save_company(ticker: str, db: Session = Depends(get_db)):
    profile = get_company_profile(ticker)[0]

    existing_company = db.query(Company).filter(Company.ticker == profile["symbol"]).first()

    if existing_company:
        existing_company.name = profile["companyName"]
        existing_company.sector = profile.get("sector")
        db.commit()
        db.refresh(existing_company)
        return existing_company

    new_company = Company(
        ticker=profile["symbol"],
        name=profile["companyName"],
        sector=profile.get("sector"),
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company
