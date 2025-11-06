import os
from crewai import Crew, Process
# Import the agents
from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor
# Import the task creation function
from stock_tasks import create_tasks
# Make sure to load environment variables, e.g., from a .env file
from dotenv import load_dotenv
load_dotenv()

# ==================== MAIN EXECUTION ====================

def analyze_stock(company_ticker: str):
    """
    Main function to run the multi-agent stock analysis
    """
     # Check for API key
    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("Please set your API key before running the crew.")
        # You might want to exit or raise an error here
        return "ERROR: Missing API key."

    print(f"\n{'='*60}")
    print(f"Starting Stock Analysis for: {company_ticker.upper()}")
    print(f"{'='*60}\n")

    # Create tasks
    tasks = create_tasks(company_ticker.upper())

    # Create crew
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


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Example: Analyze Apple stock
    company_input = input("Enter company stock ticker (e.g., AAPL, TSLA, MSFT): ")

    if company_input:
        analyze_stock(company_input)
    else:
        print("No ticker provided. Analyzing AAPL as example...")
        analyze_stock("AAPL")

