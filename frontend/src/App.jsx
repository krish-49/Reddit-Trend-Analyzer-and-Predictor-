import { useState } from "react";

export default function App() {
  const [title, setTitle] = useState("");
  const [selftext, setSelftext] = useState("");
  const [hour, setHour] = useState(12);
  const [day, setDay] = useState("Monday");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const predict = async () => {
    if (!title.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          selftext,
          hour,
          dayofweek: day,
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Backend not running or network error");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 px-4">
      <div className="bg-white w-full max-w-xl p-8 rounded-2xl shadow-2xl">
        <h1 className="text-4xl font-bold text-center text-orange-600 mb-6">
          Reddit Trend Predictor
        </h1>

        {/* Title */}
        <input
          type="text"
          placeholder="Post Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-3 border rounded-lg mb-3 focus:outline-none focus:ring-2 focus:ring-orange-500"
        />

        {/* Description */}
        <textarea
          placeholder="Post Description"
          value={selftext}
          onChange={(e) => setSelftext(e.target.value)}
          className="w-full p-3 border rounded-lg mb-3 h-28 resize-none focus:outline-none focus:ring-2 focus:ring-orange-500"
        />

        {/* Hour */}
        <label className="block text-sm font-semibold mb-1">Hour of Day</label>
        <input
          type="number"
          min="0"
          max="23"
          value={hour}
          onChange={(e) => setHour(Number(e.target.value))}
          className="w-full p-3 border rounded-lg mb-3 focus:outline-none focus:ring-2 focus:ring-orange-500"
        />

        {/* Day */}
        <label className="block text-sm font-semibold mb-1">Day of Week</label>
        <select
          value={day}
          onChange={(e) => setDay(e.target.value)}
          className="w-full p-3 border rounded-lg mb-5 focus:outline-none focus:ring-2 focus:ring-orange-500"
        >
          {[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
          ].map((d) => (
            <option key={d}>{d}</option>
          ))}
        </select>

        {/* Predict Button */}
        <button
          onClick={predict}
          className="w-full bg-orange-600 text-white py-3 rounded-lg font-semibold hover:bg-orange-700 transition duration-200"
        >
          {loading ? "Predicting..." : "Predict"}
        </button>

        {/* Result */}
        {result && (
          <div className="mt-6 p-4 bg-gray-100 rounded-xl text-center">
            <h3 className="text-lg font-semibold">
              Trend Probability: {result.trend_probability}%
            </h3>
            <p className="font-bold mt-1">Status: {result.label}</p>
          </div>
        )}
      </div>
    </div>
  );
}
