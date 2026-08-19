import yfinance as yf

def get_company_profile(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "symbol": info.get("symbol"),
        "companyName": info.get("longName"),
        "sector": info.get("sector"),
        "price": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
    }

def get_income_statement(ticker: str, period: str = "annual", limit: int = 5):
    stock = yf.Ticker(ticker)
    statement = stock.income_stmt if period == "annual" else stock.quarterly_income_stmt
    statement = statement.iloc[:, :limit]
    statement.columns = [str(col.date()) for col in statement.columns]
    return statement.to_dict()

def get_balance_sheet(ticker: str, period: str = "annual", limit: int = 5):
    stock = yf.Ticker(ticker)
    statement = stock.balance_sheet if period == "annual" else stock.quarterly_balance_sheet
    statement = statement.iloc[:, :limit]
    statement.columns = [str(col.date()) for col in statement.columns]
    return statement.to_dict()

def get_cash_flow(ticker: str, period: str = "annual", limit: int = 5):
    stock = yf.Ticker(ticker)
    statement = stock.cashflow if period == "annual" else stock.quarterly_cashflow
    statement = statement.iloc[:, :limit]
    statement.columns = [str(col.date()) for col in statement.columns]
    return statement.to_dict()


def project_future_cash_flows(ticker: str, years: int = 5, growth_rate: float = 0.08):
    cash_flow_data = get_cash_flow(ticker)
    most_recent_period = list(cash_flow_data.keys())[0]
    latest_fcf = cash_flow_data[most_recent_period]["Free Cash Flow"]

    projected = []
    for year in range(1, years + 1):
        projected_fcf = latest_fcf * (1 + growth_rate) ** year
        projected.append(projected_fcf)

    return projected



def get_full_dcf_valuation(ticker: str, growth_rate: float = 0.08, perpetual_growth_rate: float = 0.025):
    wacc_data = get_company_wacc(ticker)
    discount_rate = wacc_data["wacc"]

    projected_cash_flows = project_future_cash_flows(ticker, years=5, growth_rate=growth_rate)
    valuation = dcf_value(projected_cash_flows, discount_rate, perpetual_growth_rate)
    return {
        "ticker": ticker,
        "projected_cash_flows": projected_cash_flows,
        "discount_rate": discount_rate,
        "perpetual_growth_rate": perpetual_growth_rate,
        "dcf_value": valuation,
        "wacc_details": wacc_data,
    }


def find_latest_valid_value(data: dict, field: str):
    for period in data.keys():
        value = data[period].get(field)
        if value is not None and value == value:  # filters out both None and nan
            return value
    return None


def get_company_wacc(ticker: str, risk_free_rate: float = 0.04, equity_risk_premium: float = 0.055):
    stock = yf.Ticker(ticker)
    info = stock.info

    market_cap = info.get("marketCap")
    beta = info.get("beta", 1.0)

    balance_sheet_data = get_balance_sheet(ticker)
    most_recent_period = list(balance_sheet_data.keys())[0]
    total_debt = balance_sheet_data[most_recent_period]["Total Debt"]

    income_data = get_income_statement(ticker)
    tax_rate = income_data[most_recent_period]["Tax Rate For Calcs"]
    interest_expense = abs(find_latest_valid_value(income_data, "Interest Expense"))

    cost_of_equity = risk_free_rate + beta * equity_risk_premium
    cost_of_debt = interest_expense / total_debt

    total_value = market_cap + total_debt
    equity_weight = market_cap / total_value
    debt_weight = total_debt / total_value

    wacc = WACC(equity_weight, debt_weight, cost_of_equity, cost_of_debt, tax_rate)

    return {
        "ticker": ticker,
        "market_cap": market_cap,
        "total_debt": total_debt,
        "beta": beta,
        "cost_of_equity": cost_of_equity,
        "cost_of_debt": cost_of_debt,
        "tax_rate": tax_rate,
        "equity_weight": equity_weight,
        "debt_weight": debt_weight,
        "wacc": wacc,
    }



def present_value(future_value: float, discount_rate: float, years: int) -> float:
     present_value = future_value / (1 + discount_rate) ** years
     return present_value

def total_present_value(cash_flows, discount_rate):
     total = 0
     for index, cf in enumerate(cash_flows):
          total = total + present_value(cf, discount_rate, index + 1)
     return total

def terminal_value(final_year_cash_flows, perpetual_growth_rate, discount_rate):
     terminal_value = final_year_cash_flows * (1 + perpetual_growth_rate) / (discount_rate - perpetual_growth_rate)
     return terminal_value

def dcf_value(cash_flows, discount_rate, perpetual_growth_rate):
    terminal_value_amount = terminal_value(cash_flows[-1], perpetual_growth_rate, discount_rate)
    discounted_terminal_value = present_value(terminal_value_amount, discount_rate, len(cash_flows))
    dcf_value = total_present_value(cash_flows, discount_rate) + discounted_terminal_value
    return dcf_value

def WACC(equity_weight, debt_weight, cost_of_equity, cost_of_debt, tax_rate):
     WACC = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)
     return WACC


def search_companies(query: str, max_results: int = 8):
    results = yf.Search(query, max_results=max_results).quotes
    return [
        {"ticker": r.get("symbol"), "name": r.get("shortname") or r.get("longname")}
        for r in results
        if r.get("symbol") and (r.get("shortname") or r.get("longname"))
    ]



import os
from anthropic import Anthropic

def generate_company_summary(ticker: str):
    profile = get_company_profile(ticker)
    income = get_income_statement(ticker, limit=3)
    balance = get_balance_sheet(ticker, limit=1)
    cash_flow = get_cash_flow(ticker, limit=1)

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = f"""Write a concise investment summary for {profile.get('companyName')} ({ticker}) in 5-6 sentences.

Company profile:
- Sector: {profile.get('sector')}
- Current price: {profile.get('price')}
- Market cap: {profile.get('marketCap')}

Income statement (last 3 periods): {income}
Balance sheet (most recent): {balance}
Cash flow (most recent): {cash_flow}

Cover: what the company does, the key revenue/earnings trend (with 1-2 specific numbers), and one notable balance sheet or cash flow characteristic. Be direct and factual — no headers, no bullet points, just plain sentences. Keep it under 150 words total."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"ticker": ticker, "summary": message.content[0].text}




def get_live_quotes(tickers: list[str]):
    data = yf.Tickers(" ".join(tickers))
    results = []
    for ticker in tickers:
        info = data.tickers[ticker].fast_info
        price = info.get("lastPrice")
        prev_close = info.get("previousClose")
        if price is None or prev_close is None or prev_close == 0:
            continue
        change_pct = ((price - prev_close) / prev_close) * 100
        results.append({
            "ticker": ticker,
            "price": f"{price:.2f}",
            "change": f"{change_pct:+.1f}%",
            "color": "#0F6E56" if change_pct >= 0 else "#A32D2D",
        })



    return results