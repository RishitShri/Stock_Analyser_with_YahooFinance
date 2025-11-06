from crewai import Task
from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor



def create_tasks(company_ticker: str):
    """Create tasks for analyzing the given stock ticker"""

    task1 = Task(
        description=f"""Collect comprehensive stock data for {company_ticker}.
        Gather 3-month historical data, current price, volume, market cap,
        P/E ratio, and other key financial metrics.""",
        agent=data_collector,
        expected_output="Detailed stock data report with all key metrics"
    )

    task2 = Task(
        description=f"""Perform technical analysis on {company_ticker}.
        Calculate and interpret moving averages, RSI, MACD, and identify
        current trends. Determine if technical indicators suggest bullish
        or bearish momentum.""",
        agent=technical_analyst,
        expected_output="Technical analysis report with indicator interpretations"
    )

    task3 = Task(
        description=f"""Analyze recent news and market sentiment for {company_ticker}.
        Review recent headlines and assess overall market sentiment.""",
        agent=news_analyst,
        expected_output="News sentiment summary"
    )

    task4 = Task(
        description=f"""Based on all collected data, technical analysis, and news sentiment,
        provide a final investment recommendation for {company_ticker}.

        Your recommendation must include:
        1. Brief overview of stock performance over the past 3 months
        2. Key strengths and risks
        3. Clear recommendation: BUY, SELL, or HOLD
        4. Reasoning for your recommendation
        5. Risk level assessment (Low/Medium/High)

        Be specific and actionable.""",
        agent=investment_advisor,
        expected_output="Final investment recommendation with BUY/SELL/HOLD decision",
        context=[task1, task2, task3]
    )

    return [task1, task2, task3, task4]


