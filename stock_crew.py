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
load_dotenv()


def analyze_stock(company_ticker: str):
    """
    Main function to run the multi-agent stock analysis
    """

    # ✅ Validate API key (STRICT)
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not set in environment")

    # ✅ Clean ticker input
    if not company_ticker or not company_ticker.strip():
        raise ValueError("Ticker cannot be empty")

    ticker = company_ticker.upper().strip()

    print(f"\n{'='*60}")
    print(f"Starting Stock Analysis for: {ticker}")
    print(f"{'='*60}\n")

    try:
        # ✅ Create tasks using ticker ONLY
        tasks = create_tasks(ticker)

        # ✅ Create crew
        crew = Crew(
            agents=[
                data_collector,
                technical_analyst,
                news_analyst,
                investment_advisor
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        # ✅ Run crew (NO inputs dict)
        result = crew.kickoff(inputs={
           "ticker": company_ticker
        })

        print(f"\n{'='*60}")
        print("FINAL RECOMMENDATION")
        print(f"{'='*60}\n")
        print(result)

        return result

    except Exception as e:
        # 🚨 IMPORTANT: Stop hallucination
        raise ValueError(f"Stock analysis failed for {ticker}: {str(e)}")


# ✅ Local testing only (safe)
if __name__ == "__main__":

    company_input = input("Enter company stock ticker (e.g., AAPL, TSLA, MSFT): ")

    if not company_input:
        print("❌ No ticker provided. Exiting...")
    else:
        try:
            analyze_stock(company_input)
        except Exception as e:
            print(f"Error: {e}")
