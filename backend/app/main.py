from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.fmp_service import get_company_profile, get_income_statement, get_balance_sheet, get_cash_flow, get_full_dcf_valuation, search_companies, get_live_quotes, generate_company_summary

from app.db.session import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-silver-sun.reflex.run"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        try:
            return get_full_dcf_valuation(ticker)
        except Exception as e:
            if "rate limit" in str(e).lower() or "too many requests" in str(e).lower():
                return {"error": "FMP is rate limiting requests right now. Please try again in a minute."}
            return {"error": f"Could not fetch valuation: {str(e)}"}

@app.get("/search/{query}")
def search(query: str):
    return search_companies(query)

@app.get("/quotes/{tickers}")
def quotes(tickers: str):
    return get_live_quotes(tickers.split(","))

@app.get("/ai/{ticker}/summary")
def ai_summary(ticker: str):
    return generate_company_summary(ticker)

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