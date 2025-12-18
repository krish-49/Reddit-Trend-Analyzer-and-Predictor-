import { useState } from "react";

function App() {
  const [title, setTitle] = useState("");
  const [selftext, setSelftext] = useState("");
  const [hour, setHour] = useState(12);
  const [day, setDay] = useState("Monday");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const predict = async () => {
    setLoading(true);
    setResult(null);

    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        selftext,
        hour,
        dayofweek: day
      })
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1 className='text-4xl sm:text-5xl lg:text-[66px] font-cinzel text-center px-4'>Reddit Trend Predictor</h1>

      <input
        placeholder="Post Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{ width: "100%", marginBottom: "10px" }}
      />

      <textarea
        placeholder="Post Description"
        value={selftext}
        onChange={(e) => setSelftext(e.target.value)}
        style={{ width: "100%", height: "100px", marginBottom: "10px" }}
      />

      <label>Hour of Day</label>
      <input
        type="number"
        min="0"
        max="23"
        value={hour}
        onChange={(e) => setHour(Number(e.target.value))}
        style={{ width: "100%", marginBottom: "10px" }}
      />

      <label>Day of Week</label>
      <select
        value={day}
        onChange={(e) => setDay(e.target.value)}
        style={{ width: "100%", marginBottom: "20px" }}
      >
        {["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
          .map(d => <option key={d}>{d}</option>)}
      </select>

      <button onClick={predict}>
        Predict
      </button>

      {loading && <p>Predicting...</p>}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Trend Probability: {result.trend_probability}%</h3>
          <strong>Status: {result.label}</strong>
        </div>
      )}
    </div>
  );
}

export default App;
