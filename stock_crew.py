import os
import re
from crewai import Crew, Process
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Import agents
from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor

# Import tasks
from stock_tasks import create_tasks

load_dotenv()

app = FastAPI()


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
        agents=[data_collector, technical_analyst, news_analyst, investment_advisor],
        tasks=tasks,
        process=Process.sequential,
        verbose=False   # 🔥 important
    )

    result = crew.kickoff()

    return str(result)


# ---------------- HELPER (STRUCTURED PARSING) ---------------- #

def extract_field(pattern, text, default=""):
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else default


# ---------------- API ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Stock Analyzer API Running"}


@app.post("/analyze")
def analyze(request: StockRequest):
    try:
        result = analyze_stock(request.ticker)

        # -------- Extract structured fields -------- #

        # Action
        action = "HOLD"
        if "BUY" in result.upper():
            action = "BUY"
        elif "SELL" in result.upper():
            action = "SELL"

        # Risk
        risk = extract_field(r"Risk Level.*?:\s*(Low|Medium|High)", result, "Medium")

        # Sections
        summary = extract_field(r"1\.\s*(.*?)\n2\.", result)
        strengths_raw = extract_field(r"Strengths:(.*?)Risks:", result)
        risks_raw = extract_field(r"Risks:(.*?)3\.", result)
        reasoning = extract_field(r"Reasoning.*?:\s*(.*?)\n5\.", result)

        strengths = [
            s.strip("- ").strip()
            for s in strengths_raw.split("\n")
            if s.strip()
        ]

        risks = [
            r.strip("- ").strip()
            for r in risks_raw.split("\n")
            if r.strip()
        ]

        return {
            "ticker": request.ticker.upper(),
            "action": action,
            "risk": risk,
            "summary": summary,
            "strengths": strengths,
            "risks": risks,
            "reasoning": reasoning
        }

    except Exception as e:
        return {"error": str(e)}
