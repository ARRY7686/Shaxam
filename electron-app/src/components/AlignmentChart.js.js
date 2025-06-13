import { Scatter } from 'react-chartjs-2';
import { Chart, LinearScale, PointElement, Title, Tooltip, Legend } from 'chart.js';

Chart.register(LinearScale, PointElement, Title, Tooltip, Legend);

const AlignmentChart = ({ plotData }) => {
  if (!plotData || Object.keys(plotData).length === 0) return null;

  const datasets = Object.entries(plotData).map(([song, points], i) => ({
    label: song,
    data: points,
    backgroundColor: `hsl(${i * 60}, 70%, 60%)`,
  }));

  return (
    <Scatter
      data={{ datasets }}
      options={{
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Fingerprint Alignment Plot' },
        },
        scales: {
          x: { title: { display: true, text: 'Input Clip Time (s)' } },
          y: { title: { display: true, text: 'Matched Song Time (s)' } },
        },
      }}
    />
  );
};