# Investie

**AI-powered investment research and stock valuation platform** — like a lightweight Bloomberg Terminal + Yahoo Finance + ChatGPT combo, built from scratch.

🔗 **Live Site:** [https://frontend-silver-sun.reflex.run](https://frontend-silver-sun.reflex.run)

## What it does

Investie lets you research any publicly traded company in one place:

-  **Company search** — look up any ticker by name or symbol
-  **Live market data** — real-time quotes and daily price movement, right on the homepage
-  **AI-generated investment summaries** — plain-English breakdowns of a company's financials, powered by Claude
-  **DCF valuation engine** — a real discounted cash flow model that pulls live financial data and calculates intrinsic value, WACC, and growth assumptions
-  **Markets page** — search, summarize, and value any company from a single screen

## Tech stack

**Frontend**
- Reflex — Python-based full-stack web framework
- Deployed on Reflex Cloud

**Backend**
- FastAPI — REST API serving company data, search, and valuation endpoints
- SQLAlchemy + Supabase (Postgres) — data storage
- yfinance — live market and financial data
- Anthropic API (Claude) — AI-generated company summaries
- Deployed on Render

## Core features in detail

### DCF Valuation Engine
A discounted cash flow model built from real financial statements:
- Projects future free cash flow from the latest reported figures
- Derives a real WACC (discount rate) from live market cap, beta, debt, and tax rate
- Calculates intrinsic value, discount rate, and perpetual growth rate

### AI Company Summaries
Feeds live financial data into Claude to generate a concise, readable investment summary — revenue growth, profitability, cash flow strength, and capital allocation — without the reader needing to parse raw financial statements themselves.

### Live Homepage Stock Cards
A rotating daily selection of stocks with real-time price, % change, and a sparkline, refreshed on page load.

## Running locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
reflex run
```

## AI usage disclosure

Claude was used to help design the system architecture and explain concepts behind FastAPI, Reflex, PostgreSQL, and SQLAlchemy while building this project, including line-by-line code explanations. All code was written by me; debugging and fixes were done independently by me.