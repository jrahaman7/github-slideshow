import { render, screen } from '@testing-library/react';
import App from './App';

test('renders stock ticker checker header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Stock Ticker Checker/i);
  expect(headerElement).toBeInTheDocument();
});
