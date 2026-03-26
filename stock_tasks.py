from crewai import Task
from stock_agents import data_collector, technical_analyst, news_analyst, investment_advisor


def create_tasks():
    """Create tasks for analyzing the given stock ticker"""

    task1 = Task(
        description="""
        Collect comprehensive stock data for {ticker}.

        You MUST:
        - Use Stock Data Fetcher tool
        - Gather 3-month historical data
        - Include price, volume, market cap, P/E ratio

        Do NOT guess values.
        """,
        agent=data_collector,
        expected_output="Detailed stock data report"
    )

    task2 = Task(
        description="""
        Perform technical analysis on {ticker}.

        You MUST:
        - Use Technical Analysis Tool
        - Calculate moving averages, RSI, MACD
        - Identify bullish or bearish trend

        Do NOT generate fake indicators.
        """,
        agent=technical_analyst,
        expected_output="Technical analysis report"
    )

    task3 = Task(
        description="""
        Analyze recent news for {ticker}.

        You MUST:
        - Use News Sentiment Tool
        - Summarize sentiment (positive/negative/neutral)

        Do NOT hallucinate news.
        """,
        agent=news_analyst,
        expected_output="News sentiment summary"
    )

    task4 = Task(
        description="""
        Based on ALL previous results, provide final recommendation for {ticker}.

        STRICT FORMAT:

        1. Brief overview of stock performance over the past 3 months
        2. Key strengths and risks
        3. Clear recommendation: BUY, SELL, or HOLD
        4. Reasoning for recommendation
        5. Risk level (Low/Medium/High)
        6. Actionable summary

        Use insights from:
        - Stock data
        - Technical indicators
        - News sentiment

        Do NOT add extra sections.
        """,
        agent=investment_advisor,
        expected_output="Final structured investment recommendation",
        context=[task1, task2, task3]
    )

    return [task1, task2, task3, task4]


