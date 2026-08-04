"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

class State(rx.State):
    """The app state."""

    ticker: str = ""

    dcf_result: dict = {}
 
    def set_ticker(self, value: str):
        self.ticker = value


    async def fetch_dcf(self):
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8001/fmp/{self.ticker}/get_full_dcf_valuation")
            self.dcf_result = response.json()

ALL_STOCKS = [
    {"ticker": "AAPL", "price": "196.80", "change": "+1.2%", "color": "#0F6E56", "points": "0,24 16,22 32,23 48,15 64,17 80,9 96,12 112,6 130,4"},
    {"ticker": "MSFT", "price": "428.15", "change": "+0.6%", "color": "#0F6E56", "points": "0,18 16,20 32,14 48,16 64,11 80,13 96,7 112,9 130,5"},
    {"ticker": "TSLA", "price": "241.30", "change": "-2.1%", "color": "#A32D2D", "points": "0,6 16,10 32,8 48,14 64,12 80,19 96,17 112,23 130,25"},
    {"ticker": "GOOGL", "price": "178.42", "change": "+0.9%", "color": "#0F6E56", "points": "0,22 16,20 32,21 48,16 64,18 80,12 96,14 112,8 130,7"},
    {"ticker": "AMZN", "price": "215.60", "change": "+0.4%", "color": "#0F6E56", "points": "0,20 16,18 32,19 48,14 64,16 80,10 96,13 112,7 130,6"},
    {"ticker": "NVDA", "price": "138.25", "change": "+2.8%", "color": "#0F6E56", "points": "0,26 16,20 32,18 48,10 64,14 80,6 96,9 112,3 130,2"},
    {"ticker": "META", "price": "612.10", "change": "-0.8%", "color": "#A32D2D", "points": "0,10 16,12 32,9 48,15 64,13 80,18 96,16 112,20 130,22"},
    {"ticker": "NFLX", "price": "890.45", "change": "+1.5%", "color": "#0F6E56", "points": "0,24 16,21 32,22 48,16 64,18 80,11 96,14 112,7 130,5"},
    {"ticker": "JPM", "price": "245.30", "change": "+0.3%", "color": "#0F6E56", "points": "0,18 16,17 32,18 48,15 64,16 80,12 96,13 112,9 130,8"},
    {"ticker": "V", "price": "312.75", "change": "+0.7%", "color": "#0F6E56", "points": "0,20 16,18 32,19 48,14 64,15 80,10 96,12 112,7 130,6"},
    {"ticker": "DIS", "price": "112.40", "change": "+0.5%", "color": "#0F6E56", "points": "0,20 16,18 32,19 48,15 64,17 80,11 96,13 112,8 130,6"},
    {"ticker": "KO", "price": "68.90", "change": "-0.3%", "color": "#A32D2D", "points": "0,12 16,14 32,11 48,17 64,15 80,20 96,18 112,22 130,24"},
    {"ticker": "PFE", "price": "27.15", "change": "+1.1%", "color": "#0F6E56", "points": "0,22 16,19 32,20 48,14 64,16 80,10 96,12 112,7 130,5"},
    {"ticker": "XOM", "price": "118.60", "change": "+0.8%", "color": "#0F6E56", "points": "0,19 16,17 32,18 48,13 64,15 80,10 96,11 112,7 130,6"},
    {"ticker": "WMT", "price": "91.25", "change": "+0.4%", "color": "#0F6E56", "points": "0,21 16,19 32,20 48,16 64,17 80,12 96,14 112,9 130,8"},
    {"ticker": "ORCL", "price": "184.30", "change": "+1.9%", "color": "#0F6E56", "points": "0,25 16,20 32,19 48,12 64,15 80,7 96,10 112,4 130,3"},
    {"ticker": "ADBE", "price": "402.10", "change": "-1.2%", "color": "#A32D2D", "points": "0,8 16,11 32,9 48,15 64,13 80,18 96,16 112,21 130,23"},
    {"ticker": "CRM", "price": "268.75", "change": "+0.6%", "color": "#0F6E56", "points": "0,18 16,16 32,17 48,13 64,14 80,10 96,11 112,7 130,6"},
    {"ticker": "PYPL", "price": "72.35", "change": "-0.9%", "color": "#A32D2D", "points": "0,10 16,13 32,11 48,17 64,15 80,19 96,17 112,21 130,22"      },
    {"ticker": "INTC", "price": "24.80", "change": "-1.5%", "color": "#A32D2D", "points": "0,9 16,12 32,10 48,16 64,14 80,20 96,18 112,23 130,25"},
    {"ticker": "BA", "price": "195.20", "change": "+0.7%", "color": "#0F6E56", "points": "0,20 16,18 32,19 48,14 64,16 80,11 96,13 112,8 130,7"},
    {"ticker": "COST", "price": "912.60", "change": "+0.3%", "color": "#0F6E56", "points": "0,21 16,20 32,21 48,17 64,18 80,13 96,15 112,10 130,9"},
    {"ticker": "MCD", "price": "285.40", "change": "-0.2%", "color": "#A32D2D", "points": "0,14 16,15 32,13 48,17 64,16 80,19 96,18 112,21 130,22"},
    {"ticker": "PEP", "price": "168.90", "change": "+0.5%", "color": "#0F6E56", "points": "0,19 16,17 32,18 48,14 64,15 80,11 96,12 112,8 130,7"},
    {"ticker": "T", "price": "22.45", "change": "+1.3%", "color": "#0F6E56", "points": "0,23 16,18 32,17 48,10 64,13 80,6 96,9 112,3 130,2"},
]

import random
from datetime import date

_seed = date.today().isoformat()
random.seed(_seed)
DAILY_STOCKS = random.sample(ALL_STOCKS, 15)



def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading("Investie", size="6", color="#1F1D1A"),
        rx.hstack(
            rx.link("Home", href="/", color="#1F1D1A", size="4"),
            rx.link("Markets", href="/markets", color="#1F1D1A", size="4"),
            rx.link("Watchlist", href="/watchlist", color="#1F1D1A", size="4"),
            rx.link("About", href="/about", color="#1F1D1A", size="4"),
            rx.link("Contact", href="/contact", color="#1F1D1A", size="4"),
            spacing="5",
        ),
        justify="between",
        width="100%",
        padding="1rem 2rem",
    )

def stock_card(ticker: str, price: str, change: str, change_color: str, points: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(ticker, size="3", weight="medium", color="#1F1D1A"),
            rx.text(change, size="2", weight="medium", color=change_color),
            justify="between",
            width="100%",
        ),
        rx.text(price, size="5", weight="medium", color="#1F1D1A", margin_top="6px", margin_bottom="6px"),
        rx.html(
            f"""
            <svg viewBox="0 0 130 32" style="width: 100%; height: 28px; display: block;">
                <polyline points="{points}" fill="none" stroke="{change_color}" stroke-width="1.6"/>
            </svg>
            """
        ),
        style={
            "min_width": "158px",
            "background_color": "#FFFFFF",
            "border_radius": "10px",
            "border": "0.5px solid #DDD8C8",
            "padding": "12px 14px",
        },
    )


def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
    rx.hstack(
    *[
        stock_card(s["ticker"], s["price"], s["change"], s["color"], s["points"])
        for s in DAILY_STOCKS
    ],
    spacing="3",
    overflow_x="auto",
    style={
    "scrollbar_width": "thin",
    "&::-webkit-scrollbar": {"height": "1px"},
    "&::-webkit-scrollbar-thumb": {"background_color": "#DDD8C8", "border_radius": "10px"},
},
),
    padding="2rem",
),
        rx.box(      
            rx.html(
                """
                <svg viewBox="0 0 600 200" preserveAspectRatio="none"
                     style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.16;">
                    <polyline points="0,140 40,120 80,135 120,90 160,105 200,60 240,80 280,40 320,55 360,20 400,45 440,15 480,35 520,10 560,25 600,5"
                              fill="none" stroke="#1D9E75" stroke-width="2"/>
                    <polyline points="0,170 40,165 80,175 120,150 160,160 200,130 240,145 280,115 320,125 360,100 400,110 440,85 480,95 520,70 560,80 600,60"
                              fill="none" stroke="#5F5E5A" stroke-width="1.5"/>
                </svg>
                """
            ),                    # <- new inner box, the "hero"
            rx.vstack(
                rx.heading(
                "Investie",
                size="9",
                style={"margin_top": "0"},
                ),
                rx.text(
                    "AI-powered investment research and valuation",
                    size="7",
                ),
                rx.button(
                    "Explore Markets",
                    size="4",
                    on_click=rx.redirect("/markets"),
                ),
                spacing="5",
                justify="center",
                min_height="85vh",
                style={"position": "relative", "z_index": "1"},
            ),
            style={
        "background_color": "#0D0D0D",
        "color": "#F5F1E8",
        "width": "100%",
        "position": "relative",
        "overflow": "hidden",
            },
        ),
        style={
            "background_color": "#F5F1E8",   # back to beige
            "color": "#2B2A28",
            "width": "100%",
            "min_height": "100vh",
        },
    )

def about() -> rx.Component:
    return rx.box(
        navbar(),
    rx.hstack(    
        rx.vstack(
            rx.heading(" About Investie", size="8", color="#1F1D1A"),
            rx.text(
    "Investie is a student-built, AI-powered investment research and valuation platform designed to bring "
    "institutional-grade financial analysis to anyone with a ticker symbol and a question. ",
    "At its core, Investie combines three things that are normally locked behind expensive terminals or "
    "scattered across a dozen different tools: real, structured financial data pulled directly from company "
    "filings, a fully built discounted cash flow (DCF) valuation engine, and AI-generated summaries that turn "
    "dense financial statements into plain-language insight. ",
    "The platform's backend is built with FastAPI and PostgreSQL, and connects to Financial Modeling Prep "
    "(FMP) to retrieve real income statement, balance sheet, and cash flow data for public companies. That "
    "data feeds directly into a custom-built valuation engine capable of calculating present value, terminal "
    "value, weighted average cost of capital (WACC), and a full DCF valuation from the ground up — the same "
    "core methodology used by equity research analysts and investment bankers. ",
    "On the frontend, Investie is built with Reflex, allowing the entire experience — from searching a "
    "company, to viewing its financials, to reading an AI-generated summary of its valuation — to run "
    "entirely in Python, end to end. ",
    "The goal of Investie isn't to replace professional research, but to make the process of understanding "
    "a company's fundamentals more transparent and more accessible — especially for students, early "
    "investors, and anyone curious about how valuation actually works under the hood, rather than just "
    "trusting a black-box number from a stock screener. ",
    "This project is under active development, with real-time market data, an expanded stock discovery "
    "experience, and Anthropic-powered AI analysis all part of the roadmap ahead.",
    size="4",
    color="#2B2A28",
),
            spacing="4",
        align="start",
        max_width="600px",
        ),
        rx.image(
        src="/chart.jpg",
        width="800px",
        height="800px",
        object_fit="contain",
        border_radius="12px",
        ),
        spacing="6",
        justify="between",
        padding="3rem 2rem",
    ),
        style={
            "background_color": "#F5F1E8",
            "color": "#2B2A28",
            "width": "100%",
            "min_height": "100vh",
        },
    )   

def markets() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("Research A Company", size="8", color="#1F1D1A"),
            
            rx.input(
                rx.text(State.ticker),
                placeholder="Enter a ticker (e.g. AAPL)",
                value=State.ticker,
                on_change=State.set_ticker,
        ),

            rx.button("Get Valuation", on_click=State.fetch_dcf),
            
            rx.cond(
                State.dcf_result,
                rx.vstack(
                    rx.heading(f"Valuation for {State.ticker}", size="6", color="#1F1D1A"),
                    rx.text(f"DCF Value: ${State.dcf_result['dcf_value']:,.0f}", size="4", color="#2B2A28"),
                    rx.text(f"Discount Rate (WACC): {State.dcf_result['discount_rate']:.2%}", size="4", color="#2B2A28"),
                    rx.text(f"Perpetual Growth Rate: {State.dcf_result['perpetual_growth_rate']:.2%}", size="4", color="#2B2A28"),
                    spacing="2",
                    align="start",
                )
            ),

        spacing="4",
        align="start",
        padding="3rem 2rem",
        max_width="700px",
        ),
        style={
            "background_color": "#F5F1E8",
            "color": "#2B2A28",
            "width": "100%",
            "min_height": "100vh",
        },
    )

def watchlist() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("Watchlist", size="8", color="#1F1D1A"),
            rx.text("Here are your saved tickers:", size="4", color="#2B2A28"),
            spacing="4",
            align="start",
            padding="3rem 2rem",
            max_width="700px",
        ),
        style={
            "background_color": "#F5F1E8",
            "color": "#2B2A28",
            "width": "100%",
            "min_height": "100vh",
        },
    )
    
def contact() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("Contact", size="8", color="#1F1D1A"),
            rx.text("If you see or encounter any issues please contact us at:", size="6", color="#2B2A28"),
            rx.text("xxx???", size="6", color="#2B2A28"),
            spacing="4",
            align="center",
            padding="3rem 2rem",
    
        ),
    )


app = rx.App(style={"background_color": "#F5F1E8"})
app.add_page(index)
app.add_page(about, route="/about")
app.add_page(markets, route="/markets")
app.add_page(watchlist, route="/watchlist")
app.add_page(contact, route="/contact")