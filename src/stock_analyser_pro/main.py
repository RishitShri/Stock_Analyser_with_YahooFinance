from flask import Flask, request, jsonify
import os
from datetime import datetime
from stock_analyser_pro.crew import StockAnalyserPro

app = Flask(__name__)

@app.route("/")
def home():
    return "Stock Analyzer is running 🚀"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json() or {}

        ticker = data.get("ticker", "AAPL")
        

        inputs = {
            "ticker": ticker,
            "current_year": str(datetime.now().year)
        }

        result = analyze_stock(ticker)
        clean_result = str(result)
        return jsonify({
            "status": "success",
            "ticker": ticker,
            "analysis": clean_result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
