import { useState } from "react";
import { Loader2 } from "lucide-react";

type ResultType = {
  ticker: string;
  decision: "BUY" | "SELL" | "HOLD";
  reason: string;
  trend: "UP" | "DOWN";
  strengths: string[];
  risks: string[];
};

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState<ResultType | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeStock = async () => {
    if (!ticker) {
      setError("Please enter a stock ticker");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(
        "https://stockanalyserwithyahoofinance-production.up.railway.app/analyze",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ticker }),
        }
      );

      if (!res.ok) throw new Error("Server error");

      const response = await res.json();
      const data = response.data;

      setResult({
        ticker: data.ticker,
        decision: data.action,
        reason: data.summary,
        trend: data.trend ?? (data.action === "BUY" ? "UP" : "DOWN"),
        strengths: data.strengths || [],
        risks: data.risks || [],
      });

    } catch {
      setError("Failed to fetch analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0b0f17] text-white px-4 py-10">

      {/* MAIN CONTENT */}
      <div className="flex-grow">

        {/* HEADER */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-semibold tracking-tight">
            Stock Analyzer
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Smart market insights
          </p>
        </div>

        {/* INPUT */}
        <div className="max-w-xl mx-auto mb-8">
          <div className="flex gap-2 bg-[#111827] border border-gray-800 rounded-xl p-2 transition-all duration-300 focus-within:border-blue-500/50 focus-within:shadow-md">
            <input
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              placeholder="Search stock (AAPL, TSLA...)"
              className="flex-1 bg-transparent outline-none px-3 text-sm text-gray-200 placeholder-gray-500"
              onKeyDown={(e) => e.key === "Enter" && analyzeStock()}
            />

            <button
              onClick={analyzeStock}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 transition-all duration-200 px-5 py-2 rounded-lg text-sm font-medium flex items-center gap-2 active:scale-95"
            >
              {loading && <Loader2 className="animate-spin" size={16} />}
              Analyze
            </button>
          </div>

          {error && (
            <p className="text-red-400 text-sm mt-2 animate-fade-in">
              {error}
            </p>
          )}
        </div>

        {/* LOADING */}
        {loading && (
          <div className="max-w-xl mx-auto animate-pulse space-y-4">
            <div className="h-6 bg-gray-700 rounded w-1/3"></div>
            <div className="h-20 bg-gray-800 rounded"></div>
            <div className="h-20 bg-gray-800 rounded"></div>
          </div>
        )}

        {/* RESULT */}
        {result && (
          <div className="max-w-4xl mx-auto bg-[#0f172a] border border-gray-800 rounded-lg p-6 transition-all duration-500 animate-fade-in-up hover:shadow-lg">

            {/* HEADER */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold">
                  {result.ticker}
                </h2>
                <p className="text-xs text-gray-500">
                  {result.trend === "UP" ? "Bullish" : "Bearish"}
                </p>
              </div>

              <span
                className={`text-xs px-3 py-1 rounded-md font-medium ${
                  result.decision === "BUY"
                    ? "bg-green-500/10 text-green-400"
                    : result.decision === "SELL"
                    ? "bg-red-500/10 text-red-400"
                    : "bg-yellow-500/10 text-yellow-400"
                }`}
              >
                {result.decision}
              </span>
            </div>

            {/* ANALYSIS */}
            <div className="mt-6">
              <p className="text-xs text-gray-500 mb-1">Analysis</p>
              <p className="text-sm text-gray-300 leading-relaxed">
                {result.reason}
              </p>
            </div>

            {/* STRENGTHS & RISKS */}
            <div className="grid md:grid-cols-2 gap-4 mt-6">
              {result.strengths.length > 0 && (
                <div className="bg-green-500/5 border border-green-500/10 p-4 rounded-lg transition-all duration-300 hover:translate-y-[-2px]">
                  <h3 className="text-green-400 text-sm mb-2">Strengths</h3>
                  {result.strengths.map((s, i) => (
                    <p key={i} className="text-xs text-gray-400">• {s}</p>
                  ))}
                </div>
              )}

              {result.risks.length > 0 && (
                <div className="bg-red-500/5 border border-red-500/10 p-4 rounded-lg transition-all duration-300 hover:translate-y-[-2px]">
                  <h3 className="text-red-400 text-sm mb-2">Risks</h3>
                  {result.risks.map((r, i) => (
                    <p key={i} className="text-xs text-gray-400">• {r}</p>
                  ))}
                </div>
              )}
            </div>

            {/* CHART */}
            <div className="mt-8 h-[420px] rounded-lg overflow-hidden border border-gray-800 bg-black transition-all duration-300 hover:border-blue-500/30">
              <iframe
                src={`https://s.tradingview.com/widgetembed/?symbol=${result.ticker}&interval=D&theme=dark&style=1`}
                width="100%"
                height="100%"
                frameBorder="0"
              />
            </div>

          </div>
        )}
      </div>

      {/* 🔥 FOOTER DISCLAIMER */}
      <footer className="max-w-5xl mx-auto w-full mt-12 border-t border-gray-800 pt-6 text-center">
        <p className="text-xs text-gray-500 leading-relaxed">
          <span className="font-medium text-gray-400">Disclaimer:</span> This platform is not registered with SEBI and is intended solely for informational and educational purposes. 
          The analysis provided does not constitute financial or investment advice. Users are strongly advised to conduct their own research 
          or consult a certified financial advisor before making any investment decisions.
        </p>
      </footer>

    </div>
  );
}

export default App;