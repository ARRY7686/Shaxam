import React, { useEffect, useState } from "react";
import { animate } from "animejs";
import gsap from "gsap";
import {
  Chart,
  RadialLinearScale,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from "chart.js";
import { PolarArea } from "react-chartjs-2";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

Chart.register(RadialLinearScale, ArcElement, Tooltip, Legend, Title);

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
            borderWidth: 1
          }
        ]
      }}
      options={{
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          animateRotate: true,
          animateScale: true
        },
        plugins: {
          legend: {
            position: "right",
            labels: { color: "#000", font: { size: 12 } }
          },
          title: {
            display: true,
            text: "Matched Songs",
            color: "#111",
            font: { size: 18, weight: "bold" }
          }
        },
        scales: {
          r: {
            ticks: { color: "#444" },
            grid: { color: "#ccc" },
            angleLines: { color: "#ccc" }
          }
        }
      }}
    />
  );
};

export default function App() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [spotifyUrl, setSpotifyUrl] = useState("");
  const [adding, setAdding] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    animate(".header-title", {
      opacity: [0, 1],
      transform: ["translateY(-50px)", "translateY(0px)"],
      easing: "ease-out",
      duration: 1200
    });

    gsap.to(".section", {
      opacity: 1,
      y: 0,
      stagger: 0.2,
      ease: "power2.out",
      duration: 1
    });
  }, [matches]);

  const maxConfidence = Math.max(...matches.map((m) => m.confidence || 0)) || 1;
  const normalizedMatches = matches.map((m) => ({
    ...m,
    normalized: Math.round((m.confidence / maxConfidence) * 100)
  }));

  const handleRecognize = async () => {
    setLoading(true);
    setMatches([]);

    try {
      const formData = new FormData();
      if (selectedFile) formData.append("file", selectedFile);

      const response = await fetch("http://localhost:5000/recognize", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      if (data.matches?.length > 0) {
        toast.success("Matches found!");
      } else {
        toast.info("No matches found.");
      }
      setMatches(data.matches || []);
    } catch (err) {
      console.error("Recognition failed", err);
      toast.error("Recognition failed");
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
      const res = await fetch("http://localhost:5000/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ spotify_url: spotifyUrl })
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
          <h2 className="text-2xl font-semibold mb-4 text-black">Add a Spotify Song</h2>
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
          <h2 className="text-2xl font-semibold mb-4 text-black">Recognize Audio</h2>
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
            {loading ? "Listening..." : "Recognize"}
          </button>
        </div>

        {/* Match Results */}
        <div className="section opacity-0 border border-gray-600 bg-gray-100 rounded-lg p-6 transition-opacity">
          <h2 className="text-2xl font-semibold mb-6 text-black">Match Results</h2>
          {normalizedMatches.length === 0 ? (
            <p className="text-gray-800">No matches yet. Try recognizing!</p>
          ) : (
            <div className="space-y-4">
              {normalizedMatches.map((match, i) => (
                <div
                  key={i}
                  className="p-4 border border-gray-400 bg-white rounded-lg flex justify-between items-center"
                >
                  <div>
                    <h3 className="font-bold text-lg text-black">{match.title}</h3>
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
