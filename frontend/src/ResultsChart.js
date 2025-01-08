import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

// Register required components
ChartJS.register(ArcElement, Tooltip, Legend);

const ResultsChart = ({ results }) => {
  const data = {
    labels: results.map((candidate) => candidate.name),
    datasets: [
      {
        label: 'Votes',
        data: results.map((candidate) => candidate.votes),
        backgroundColor: [
          '#FF6384', // Red
          '#36A2EB', // Blue
          '#FFCE56', // Yellow
          '#4BC0C0', // Teal
          '#9966FF', // Purple
        ],
        hoverOffset: 4,
      },
    ],
  };

  return (
    <div style={{ width: '400px', height: '400px' }}>
      <Pie data={data} />
    </div>
  );
};

export default ResultsChart;
