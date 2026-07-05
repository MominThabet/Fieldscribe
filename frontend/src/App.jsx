import { useState } from "react";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function checkBackend() {
    setError(null);
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/ping");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Could not reach the backend. Is it running on port 8000?");
    }
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Fieldscribe</h1>
      <p>Phase 0 checkpoint: confirm the frontend can talk to the backend.</p>
      <button onClick={checkBackend}>Ping backend</button>
      {result && <p>✅ {result.message}</p>}
      {error && <p>❌ {error}</p>}
    </div>
  );
}
