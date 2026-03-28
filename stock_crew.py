import os
import re
from crewai import Crew, Process
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor
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
        verbose=False
    )

    result = crew.kickoff()

    return str(result)


# ---------------- HELPER FUNCTIONS ---------------- #

def extract_field(pattern, text, default=""):
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else default


def extract_list(section_text):
    return [
        line.strip("- ").strip()
        for line in section_text.split("\n")
        if line.strip()
    ]


# ---------------- API ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "Stock Analyzer API Running"}


@app.post("/analyze")
def analyze(request: StockRequest):
    try:
        result = analyze_stock(request.ticker)

        # -------- Dynamic Extraction -------- #

        result_upper = result.upper()

        # Action (no hardcoding, detection only)
        action = next(
            (word for word in ["BUY", "SELL", "HOLD"] if word in result_upper),
            "HOLD"
        )

        # Risk
        risk = extract_field(r"Risk Level.*?:\s*(Low|Medium|High)", result, "Medium")

        # Sections
        summary = extract_field(r"1\.\s*(.*?)\n2\.", result)

        strengths_raw = extract_field(r"Strengths:(.*?)Risks:", result)
        risks_raw = extract_field(r"Risks:(.*?)3\.", result)

        strengths = extract_list(strengths_raw)
        risks = extract_list(risks_raw)

        return {
            "ticker": request.ticker.upper(),
            "action": action,
            "risk": risk,
            "summary": summary,
            "strengths": strengths,
            "risks": risks
        }

    except Exception as e:
        return {"error": str(e)}
