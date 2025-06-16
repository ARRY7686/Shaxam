import { Chart, LinearScale, PointElement, Title, Tooltip, Legend, BubbleController } from 'chart.js';
import { Scatter } from 'react-chartjs-2';

Chart.register(LinearScale, PointElement, Title, Tooltip, Legend, BubbleController);

const AlignmentChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) return null;

  const { spectrogram, alignments } = data;

  const spectrogramDataset = {
    label: 'Spectrogram',
    data: spectrogram.map(({ x, y, value }) => ({
      x,
      y,
      r: Math.max(1, (value + 80) / 15) // adjust for visual scale
    })),
    backgroundColor: 'rgba(0, 123, 255, 0.3)',
    borderWidth: 0,
  };

  const alignmentDatasets = Object.entries(alignments).map(([song, points], i) => ({
    label: song,
    data: points,
    backgroundColor: `hsl(${i * 60}, 70%, 50%)`,
    pointRadius: 4,
    type: 'scatter',
  }));

  return (
    <Scatter
      data={{
        datasets: [spectrogramDataset, ...alignmentDatasets],
      }}
      options={{
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Spectrogram with Fingerprint Alignments' },
        },
        scales: {
          x: { title: { display: true, text: 'Time (s)' } },
          y: { title: { display: true, text: 'Frequency (Hz)' } },
        },
      }}
    />
  );
};

export default AlignmentChart;
