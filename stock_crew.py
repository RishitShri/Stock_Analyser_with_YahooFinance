import os
import json
from crewai import Crew, Process
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor
from stock_tasks import create_tasks

load_dotenv()

app = FastAPI()

# ---------------- CORS (REQUIRED FOR FRONTEND) ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- REQUEST MODEL ---------------- #

class StockRequest(BaseModel):
    ticker: str


# ---------------- CORE FUNCTION ---------------- #

def analyze_stock(company_ticker: str):

    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not set")

    ticker = company_ticker.upper().strip()

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
        verbose=False
    )

    result = crew.kickoff()

    return str(result)


# ---------------- API ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Stock Analyzer API Running"}


@app.post("/analyze")
def analyze(request: StockRequest):
    try:
        result = analyze_stock(request.ticker)

        cleaned = result.strip()

      
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("Invalid JSON format from LLM")

        json_str = cleaned[start:end]
        parsed = json.loads(json_str)

        return {
            "success": True,
            "data": {
                "ticker": request.ticker.upper(),
                "action": parsed.get("action", "").upper(),
                "risk": parsed.get("risk", "").upper(),
                "summary": parsed.get("summary", ""),
                "strengths": parsed.get("strengths", []),
                "risks": parsed.get("risks", [])
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
