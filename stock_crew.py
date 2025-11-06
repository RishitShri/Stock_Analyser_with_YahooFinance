import os
from crewai import Crew, Process

from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor

from stock_tasks import create_tasks

from dotenv import load_dotenv
load_dotenv()


def analyze_stock(company_ticker: str):
    """
    Main function to run the multi-agent stock analysis
    """
   
    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("Please set your API key before running the crew.")
        return "ERROR: Missing API key."

    print(f"\n{'='*60}")
    print(f"Starting Stock Analysis for: {company_ticker.upper()}")
    print(f"{'='*60}\n")


    tasks = create_tasks(company_ticker.upper())

 
    crew = Crew(
        agents=[data_collector, technical_analyst, news_analyst, investment_advisor],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    result = crew.kickoff()

    print(f"\n{'='*60}")
    print("FINAL RECOMMENDATION")
    print(f"{'='*60}\n")
    print(result)

    return result



if __name__ == "__main__":
   
    company_input = input("Enter company stock ticker (e.g., AAPL, TSLA, MSFT): ")

    if company_input:
        analyze_stock(company_input)
    else:
        print("No ticker provided. Analyzing AAPL as example...")
        analyze_stock("AAPL")


