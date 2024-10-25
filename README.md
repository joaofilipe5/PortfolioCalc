Simple Sharpe and Sortino Ratio Calculator for Portfolio

Overview

This project is a Python-based tool designed to calculate key risk-adjusted performance metrics for individual stocks and a portfolio. Specifically, it calculates the Sharpe Ratio, Sortino Ratio, Beta, and Treynor Ratio for a portfolio of stocks. The tool pulls historical stock data using the yfinance library and handles portfolio-level and stock-level performance analytics.

The core functionality is encapsulated in two classes:

	•	Stock: Represents an individual stock with methods to calculate key metrics like Sharpe and Sortino ratios.
	•	Portfolio: Represents a collection of stocks and can calculate portfolio-wide metrics such as Beta, Sharpe, and Sortino ratios.

Key Features:

	•	Fetch historical data from Yahoo Finance using the yfinance API.
	•	Calculate Sharpe and Sortino ratios for both individual stocks and the entire portfolio.
	•	Calculate portfolio beta and Treynor ratio.
	•	Export detailed stock data and portfolio summary to an Excel file.
