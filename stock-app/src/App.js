import React, { useState } from 'react';
import './App.css';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_KEY = 'pHXO4k6bsRZFwRibHLiZ3_6h7K9RGIEl';

function App() {
  const [ticker, setTicker] = useState('');
  const [stockData, setStockData] = useState(null);
  const [earningsData, setEarningsData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTickerChange = (event) => {
    setTicker(event.target.value.toUpperCase());
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setStockData(null);
    setEarningsData(null);
    setChartData(null);

    const today = new Date();
    const fiveYearsAgo = new Date(new Date().setFullYear(today.getFullYear() - 5));
    const fromDate = fiveYearsAgo.toISOString().slice(0, 10);
    const toDate = today.toISOString().slice(0, 10);

    const aggregatesUrl = `https://api.polygon.io/v2/aggs/ticker/${ticker}/range/1/day/${fromDate}/${toDate}?adjusted=true&sort=asc&limit=5000&apiKey=${API_KEY}`;
    const financialsUrl = `https://api.polygon.io/vX/reference/financials?ticker=${ticker}&limit=20&apiKey=${API_KEY}`;

    try {
      const [aggsResponse, financialsResponse] = await Promise.all([
        fetch(aggregatesUrl),
        fetch(financialsUrl)
      ]);

      if (!aggsResponse.ok || !financialsResponse.ok) {
        throw new Error('Failed to fetch data. Please check the ticker symbol.');
      }

      const aggsData = await aggsResponse.json();
      const financialsData = await financialsResponse.json();

      if (aggsData.results && aggsData.results.length > 0) {
        const highs = aggsData.results.map(result => result.h);
        const lows = aggsData.results.map(result => result.l);
        const fiveYearHigh = Math.max(...highs);
        const fiveYearLow = Math.min(...lows);
        setStockData({ high: fiveYearHigh, low: fiveYearLow });

        const labels = aggsData.results.map(result => new Date(result.t).toLocaleDateString());
        const data = aggsData.results.map(result => result.c);
        setChartData({
          labels,
          datasets: [
            {
              label: `${ticker} Closing Price`,
              data,
              fill: false,
              backgroundColor: 'rgb(75, 192, 192)',
              borderColor: 'rgba(75, 192, 192, 0.2)',
            },
          ],
        });

      } else {
        setStockData({ high: 'N/A', low: 'N/A' });
      }

      if (financialsData.results && financialsData.results.length > 0) {
        setEarningsData(financialsData.results);
      } else {
        setEarningsData([]);
      }

    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Stock Ticker Checker</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={ticker}
            onChange={handleTickerChange}
            placeholder="Enter stock ticker (e.g., AAPL)"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Fetching...' : 'Get Stock Info'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {chartData && (
          <div className="chart-container">
            <Line data={chartData} />
          </div>
        )}

        {stockData && (
          <div className="stock-info">
            <h2>Stock Performance (5 Years)</h2>
            <div className="performance-data">
              <p>5-Year High: {stockData.high}</p>
              <p>5-Year Low: {stockData.low}</p>
            </div>
          </div>
        )}

        {earningsData && (
          <div className="stock-info">
            <h2>Quarterly Earnings</h2>
            <div className="earnings-data">
              {earningsData.length > 0 ? (
                <ul>
                  {earningsData.map((earning, index) => (
                    <li key={index}>
                      <strong>{earning.end_date}:</strong> Revenue: {earning.financials.income_statement.revenues.value} {earning.financials.income_statement.revenues.unit}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No earnings data available.</p>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
