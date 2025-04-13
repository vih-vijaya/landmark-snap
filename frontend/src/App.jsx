import { useState } from 'react';
import './App.css';

function App() {
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://localhost:8000/api/predict/", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📸 Landmark Snap Lite</h1>

      <input type="file" accept="image/*" onChange={handleUpload} />

      {preview && (
        <div style={{ marginTop: "1rem" }}>
          <img src={preview} alt="preview" style={{ maxWidth: "300px", borderRadius: "8px" }} />
        </div>
      )}

      {loading && <p>⏳ Predicting...</p>}

      {result && (
        <div style={{ marginTop: "1rem", textAlign: "left" }}>
          <h3>🪧 Prediction: <strong>{result.predicted_place}</strong></h3>
          <p>📍 From: {result.from}</p>

          <h4>🚗 Road Travel</h4>
          {result.travel_modes.road.error ? (
            <p style={{ color: "red" }}>{result.travel_modes.road.error}</p>
          ) : (
            <>
              <p>🛣️ Distance: {result.travel_modes.road.distance_km} km</p>
              <p>⏱️ Duration: {result.travel_modes.road.duration}</p>
              <p>💰 Estimated Cost: ${result.travel_modes.road.estimated_cost_usd}</p>
            </>
          )}

          <h4>✈️ Flight Travel</h4>
          <p>🛫 Distance: {result.travel_modes.flight.distance_km} km</p>
          <p>💸 Estimated Cost: ${result.travel_modes.flight.estimated_cost_usd}</p>

          <h4>📝 Description</h4>
          <p>{result.caption}</p>
        </div>
      )}
    </div>
  );
}

export default App;
