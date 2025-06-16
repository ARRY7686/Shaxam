import React from "react";
import { Scatter } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(LinearScale, PointElement, Tooltip, Legend);

const SpectrogramChart = ({ data }) => {
  if (!data) {
    console.warn("⚠️ No data prop passed to SpectrogramChart.");
    return null;
  }

  const { spectrogram, alignments } = data;

  console.log("📊 SpectrogramChart Debug Info:");
  console.log("→ spectrogram length:", spectrogram?.length);
  console.log("→ alignment keys:", Object.keys(alignments || {}));

  const fallbackSpectrogram = [
    { x: 1, y: 1000, r: 5 },
    { x: 2, y: 2000, r: 8 },
    { x: 3, y: 3000, r: 10 }
  ];

  const spectrogramPoints = Array.isArray(spectrogram)
    ? spectrogram
        .filter(
          (p, i) =>
            i % 3 === 0 &&
            p &&
            typeof p.x === "number" &&
            typeof p.y === "number" &&
            typeof p.value === "number"
        )
        .map((p) => ({
          x: p.x,
          y: p.y,
          r: Math.max(1, (p.value + 100) / 20)
        }))
    : fallbackSpectrogram;

  // ✅ Fixed reducer logic to pick best match correctly
  const alignmentEntries = Object.entries(alignments || {});
  const bestMatch = alignmentEntries.reduce(
    (best, [label, points]) => {
      if (!Array.isArray(points)) return best;
      return points.length > best.points.length
        ? { label, points }
        : best;
    },
    { label: null, points: [] }
  );

  console.log("🎯 Corrected Best match label:", bestMatch.label);
  console.log("🎯 Corrected Best match points:", bestMatch.points.length);

  const bestAlignmentDataset = bestMatch.label
    ? [
        {
          label: `Matched: ${bestMatch.label}`,
          data: bestMatch.points.map((p) => ({ x: p.x, y: p.y })),
          backgroundColor: "hsl(220, 100%, 50%)",
          pointRadius: 4,
          type: "scatter"
        }
      ]
    : [];

  return (
    <Scatter
      data={{
        datasets: [
          {
            label: "Spectrogram",
            data: spectrogramPoints,
            backgroundColor: "rgba(255, 99, 132, 0.3)",
            type: "bubble"
          },
          ...bestAlignmentDataset
        ]
      }}
      options={{
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                const point = ctx.raw;
                const x = point?.x?.toFixed(2);
                const y = point?.y?.toFixed(2);
                const r = point?.r?.toFixed?.(2);
                return r ? `x: ${x}, y: ${y}, r: ${r}` : `x: ${x}, y: ${y}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Time (s)" },
            min: 0,
            max: 40
          },
          y: {
            title: { display: true, text: "Frequency (Hz)" },
            min: 0,
            max: 12000
          }
        }
      }}
    />
  );
};

export default SpectrogramChart;
