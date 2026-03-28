import os
from crewai import Crew, Process

from stock_agents import (
    data_collector,
    technical_analyst,
    news_analyst,
    investment_advisor
)

from stock_tasks import create_tasks

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

# ---------------- API SETUP ---------------- #

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str


# ---------------- CORE FUNCTION ---------------- #

def analyze_stock(company_ticker: str):

    # ✅ Validate API key
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not set in environment")

    if not company_ticker or not company_ticker.strip():
        raise ValueError("Ticker cannot be empty")

    ticker = company_ticker.upper().strip()

    try:
        tasks = create_tasks(ticker)

        crew = Crew(
            agents=[
                data_collector,
                technical_analyst,
                news_analyst,
                investment_advisor
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=False   # 🔥 IMPORTANT FIX
        )

        result = crew.kickoff(inputs={
            "ticker": ticker
        })

        return str(result)   # 🔥 ensure clean output

    except Exception as e:
        raise ValueError(f"Stock analysis failed for {ticker}: {str(e)}")


# ---------------- API ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Stock Analyzer API Running"}


@app.post("/analyze")
def analyze(request: StockRequest):
    try:
        result = analyze_stock(request.ticker)

        return {
            "ticker": request.ticker,
            "recommendation": result
        }

    except Exception as e:
        return {"error": str(e)}
