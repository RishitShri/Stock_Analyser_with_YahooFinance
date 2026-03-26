from flask import Flask, request, jsonify
import os
from stock_analyser_pro.crew import analyze_stock  # IMPORTANT

app = Flask(__name__)

@app.route("/")
def home():
    return "Stock Analyzer is running 🚀"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        # ✅ Strict validation (NO default)
        if not data or "ticker" not in data:
            return jsonify({
                "status": "error",
                "message": "Ticker is required"
            }), 400

        ticker = data["ticker"].upper().strip()

        # ✅ Call your crew properly
        result = analyze_stock(ticker)

        return jsonify({
            "status": "success",
            "ticker": ticker,
            "analysis": str(result)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
