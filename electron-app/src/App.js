import React, { useEffect, useState } from "react";
import { animate } from "animejs";
import gsap from "gsap";
import {
  Chart,
  RadialLinearScale,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import { PolarArea } from "react-chartjs-2";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import SpectrogramChart from "./components/SpectogramChart";
import "./App.css";

Chart.register(RadialLinearScale, ArcElement, Tooltip, Legend, Title);
const API_BASE_URL = "http://localhost:5000";

const MatchConfidencePolarChart = ({ matches }) => {
  if (!matches || matches.length === 0) return null;

  const labels = matches.map((m) =>
    m.title.length > 25 ? m.title.slice(0, 25) + "…" : m.title
  );

  const data = matches.map((m) => m.normalized);
  const backgroundColors = labels.map(
    (_, i) => `hsl(${(i * 360) / labels.length}, 40%, 50%)`
  );

  return (
    <PolarArea
      data={{
        labels,
        datasets: [
          {
            label: "Confidence (%)",
            data,
            backgroundColor: backgroundColors,
            borderColor: "#111",
            borderWidth: 1,
          },
        ],
      }}
      options={{
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          animateRotate: true,
          animateScale: true,
        },
        plugins: {
          legend: {
            position: "right",
            labels: { color: "#000", font: { size: 12 } },
          },
          title: {
            display: true,
            text: "Matched Songs",
            color: "#111",
            font: { size: 18, weight: "bold" },
          },
        },
        scales: {
          r: {
            ticks: { color: "#444" },
            grid: { color: "#ccc" },
            angleLines: { color: "#ccc" },
          },
        },
      }}
    />
  );
};

export default function App() {
  const [matches, setMatches] = useState([]);
  const [plotData, setPlotData] = useState(null); // 🆕
  const [specData, setSpecData] = useState(null); // 🆕
  const [loading, setLoading] = useState(false);
  const [spotifyUrl, setSpotifyUrl] = useState("");
  const [adding, setAdding] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    animate(".header-title", {
      opacity: [0, 1],
      transform: ["translateY(-50px)", "translateY(0px)"],
      easing: "ease-out",
      duration: 1200,
    });

    gsap.to(".section", {
      opacity: 1,
      y: 0,
      stagger: 0.2,
      ease: "power2.out",
      duration: 1,
    });
  }, [matches]);

  const maxConfidence = Math.max(...matches.map((m) => m.confidence || 0)) || 1;
  const normalizedMatches = matches.map((m) => ({
    ...m,
    normalized: Math.round((m.confidence / maxConfidence) * 100),
  }));

  const handleRecognize = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/recognize`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMatches(data.matches || []);
      setPlotData(data.plot_data || {}); // 🆕

      // 🔥 Minimal addition: fetch spectrogram
      const specRes = await fetch(`${API_BASE_URL}/spectrogram`);
      const specJson = await specRes.json();
      setSpecData(specJson); // 🆕
    } catch (error) {
      console.error("Recognition failed:", error);
      setMatches([]);
      setPlotData(null); // 🆕
      setSpecData(null); // 🆕
    }
    setLoading(false);
  };

  const handleAddSong = async () => {
    if (!spotifyUrl.trim()) {
      toast.warning("Please enter a Spotify URL");
      return;
    }
    setAdding(true);
    try {
      const res = await fetch(`${API_BASE_URL}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ spotify_url: spotifyUrl }),
      });
      const data = await res.json();
      if (res.ok) {
        toast.success("Song added successfully!");
        setSpotifyUrl("");
      } else {
        toast.error(data.error || "Failed to add song");
      }
    } catch (err) {
      console.error("Add failed", err);
      toast.error("Failed to add song");
    }
    setAdding(false);
  };

  return (
    <div className="min-h-screen bg-white text-black font-sans p-6">
      <header className="text-center py-12">
        <h1 className="header-title text-5xl font-black tracking-tight opacity-0">
          Shaxam 🎧
        </h1>
        <p className="text-lg mt-2 text-gray-800">
          Audio Fingerprinting, Simplified.
        </p>
      </header>

      <div className="max-w-4xl mx-auto space-y-12">
        {/* Add Track */}
        <div className="section opacity-0 border border-gray-600 bg-gray-100 rounded-lg p-6 transition-opacity">
          <h2 className="text-2xl font-semibold mb-4 text-black">
            Add a Spotify Song
          </h2>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Enter Spotify track URL"
              value={spotifyUrl}
              onChange={(e) => setSpotifyUrl(e.target.value)}
              className="flex-1 border border-gray-600 px-4 py-2 rounded bg-white text-black"
            />
            <button
              onClick={handleAddSong}
              className="px-4 py-2 border border-gray-800 bg-gray-900 text-white hover:bg-gray-700 transition"
            >
              {adding ? "Adding..." : "Add"}
            </button>
          </div>
        </div>

        {/* Upload + Recognize */}
        <div className="section opacity-0 border border-gray-600 bg-gray-100 rounded-lg p-6 transition-opacity">
          <h2 className="text-2xl font-semibold mb-4 text-black">
            Recognize Audio
          </h2>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setSelectedFile(e.target.files[0])}
            className="mb-4 text-black"
          />
          <button
            onClick={handleRecognize}
            className="px-6 py-2 border border-gray-800 bg-gray-900 text-white hover:bg-gray-700 transition"
          >
            {loading ? "Waiting..." : "Recognize"}
          </button>
        </div>

        {/* Match Results */}
        <div className="section opacity-0 border border-gray-600 bg-gray-100 rounded-lg p-6 transition-opacity">
          <h2 className="text-2xl font-semibold mb-6 text-black">
            Match Results
          </h2>
          {normalizedMatches.length === 0 ? (
            <p className="text-gray-800">No matches yet. Try recognizing!</p>
          ) : (
            <div className="space-y-4">
              {normalizedMatches.slice(0,4).map((match, i) => (
                <div
                  key={i}
                  className="p-4 border border-gray-400 bg-white rounded-lg flex justify-between items-center"
                >
                  <div>
                    <h3 className="font-bold text-lg text-black">
                      {match.title}
                    </h3>
                    <p className="text-sm text-gray-800">
                      Confidence: {match.normalized}%
                    </p>
                  </div>
                  <div className="h-2 w-32 bg-gray-200 rounded overflow-hidden">
                    <div
                      className="bg-black h-full"
                      style={{ width: `${match.normalized}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Polar Chart */}
        <div className="section opacity-0 border border-gray-600 bg-gray-100 rounded-lg p-6 h-[500px] transition-opacity">
          <MatchConfidencePolarChart matches={normalizedMatches} />
        </div>

        {/* Spectrogram Chart */}
        {specData && plotData && (
          <div className="section  border border-gray-600 bg-gray-100 rounded-lg p-6 transition-opacity">
            <h2 className="text-2xl font-semibold mb-4 text-black">
              Spectrogram
            </h2>
            <SpectrogramChart
              data={{
                spectrogram: specData?.spectrogram || [],
                alignments:
                  specData?.alignments && matches.length > 0
                    ? {
                        [matches[0].title]:
                          specData.alignments[matches[0].title],
                      }
                    : {},
              }}
            />
          </div>
        )}
      </div>

      {/* Toastify Container */}
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  );
}
