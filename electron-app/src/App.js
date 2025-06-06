import React, { useState } from "react";
import "./App.css"

function App() {
  const [matches, setMatches] = useState([]);
  const [plot, setPlot] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRecognize = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/recognize");
      const data = await res.json();
      setMatches(data.matches || []);
      setPlot(data.plot || "");
    } catch (err) {
      console.error("Recognition failed", err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-slate-900 text-white font-inter">
      {/* Background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent"></div>
      
      <div className="relative z-10 px-6 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-6 shadow-lg shadow-blue-500/25">
              <span className="text-3xl">🎧</span>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
              Shaxam
            </h1>
            <p className="text-gray-400 text-lg">Discover music with AI-powered recognition</p>
          </div>

          {/* Main Action Button */}
          <div className="text-center mb-12">
            <button
              onClick={handleRecognize}
              disabled={loading}
              className="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transform hover:scale-105 transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative flex items-center space-x-3">
                <span className="text-2xl">
                  {loading ? "🎙️" : "🎵"}
                </span>
                <span>
                  {loading ? "Listening..." : "Recognize Song"}
                </span>
              </div>
              {loading && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin ml-2"></div>
                </div>
              )}
            </button>
          </div>

          {/* Results Section */}
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Matches */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50 shadow-xl">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <span className="w-2 h-8 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full mr-3"></span>
                Match Results
              </h2>
              
              <div className="space-y-4">
                {matches.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="w-16 h-16 bg-gray-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl text-gray-500">🔍</span>
                    </div>
                    <p className="text-gray-400">No matches found yet</p>
                    <p className="text-sm text-gray-500 mt-2">Click the button above to start recognition</p>
                  </div>
                ) : (
                  matches.map((match, index) => (
                    <div
                      key={index}
                      className="bg-gray-700/30 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-white text-lg mb-1">
                            {match.title}
                          </h3>
                          <div className="flex items-center space-x-4">
                            <span className="text-sm text-gray-400">Confidence:</span>
                            <div className="flex items-center space-x-2">
                              <div className="w-24 h-2 bg-gray-600 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-green-500 to-blue-500 rounded-full transition-all duration-500"
                                  style={{ width: `${Math.min(match.confidence * 100, 100)}%` }}
                                ></div>
                              </div>
                              <span className="text-blue-400 font-medium">
                                {(match.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="text-2xl ml-4">🎵</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Plot Visualization */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50 shadow-xl">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <span className="w-2 h-8 bg-gradient-to-b from-green-500 to-blue-500 rounded-full mr-3"></span>
                Audio Analysis
              </h2>
              
              <div className="h-64 flex items-center justify-center">
                {plot ? (
                  <div className="w-full h-full rounded-xl overflow-hidden bg-gray-900/50 p-4">
                    <img
                      src={`data:image/png;base64,${plot}`}
                      alt="Audio analysis visualization"
                      className="w-full h-full object-contain rounded-lg"
                    />
                  </div>
                ) : (
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gray-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl text-gray-500">📊</span>
                    </div>
                    <p className="text-gray-400">Audio visualization will appear here</p>
                    <p className="text-sm text-gray-500 mt-2">Start recognition to see the analysis</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="text-center mt-12 pt-8 border-t border-gray-700/50">
            <p className="text-gray-500 text-sm">
              Powered by advanced audio fingerprinting technology
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;