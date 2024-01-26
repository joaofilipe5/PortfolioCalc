import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


class Stock():
    def __init__(self, symbol, invested, value, risk_free_rate):
        self.symbol = symbol
        self.RF = risk_free_rate
        self.value = value
        self.investment = invested
        self.data = None
    
    def getTicker(self):
        self.stock = yf.Ticker(self.symbol)
        return self.stock

    def getInvestment(self):
        return self.investment

    def getAmount(self):
        return self.value

    def get_data(self, start_date, end_date):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        self.data = yf.download(self.symbol, start=start_date, end=end_date, interval='1d')
        return self.data

    def getInfo(self):
        return self.getTicker().info

    def getBeta(self):
        return self.getInfo()['beta']

    def getClose(self):
        if self.data is None:
            self.get_data(None, None)
        return self.data['Adj Close']

    def getReturns(self):
        return self.getClose().pct_change()

    def getTotalReturn(self):
        totalReturn = (self.getClose().iloc[-1] - self.getClose().iloc[0]) / self.getClose().iloc[0]
        return totalReturn
        
    def annualToDaily(self):
        return (1 + self.RF)**(1/252) - 1

    def getExcessReturns(self):
        excessReturns = self.getReturns() - self.annualToDaily()
        return excessReturns  

    def getSharpeRatio(self):
        sharpe = self.getExcessReturns().mean() / self.getExcessReturns().std() * np.sqrt(252)
        return sharpe  

    def getSortinoRatio(self):
        downside_returns = self.getExcessReturns()[self.getExcessReturns() < 0]
        sortino = self.getExcessReturns().mean() / downside_returns.std() * np.sqrt(252)
        return sortino
    
class Portfolio():
    def __init__(self, stocks, risk_free_rate):
        self.stocks = stocks
        self.RF = risk_free_rate

    def getValue(self):
        Total = 0
        for stock in self.stocks:
            Total += stock.getAmount()
        return Total

    def getWeight(self,stock1):
        Total = 0
        for stock in self.stocks:
            Total += stock.getAmount()
        self.weight = stock1.getAmount() / Total
        return self.weight

    def getBetaP(self):
        portfolioBeta = 0
        for stock in self.stocks:
            portfolioBeta += stock.getBeta() * self.getWeight(stock)
        return  portfolioBeta

    def getReturns(self):
        portfolioReturns = 0
        for stock in self.stocks:
            portfolioReturns += stock.getTotalReturn() * self.getWeight(stock)
        return portfolioReturns
    
    def getPortfolioSharpe(self):
        portfolioSharpe = 0
        for stock in self.stocks:
            portfolioSharpe += stock.getSharpeRatio() * self.getWeight(stock)
        return portfolioSharpe

    def getPortfolioSortino(self):
        portfolioSortino = 0
        for stock in self.stocks:
            portfolioSortino += stock.getSortinoRatio() * self.getWeight(stock)
        return portfolioSortino

    def getTreynorRatio(self):
        return (self.getReturns() - self.RF) / self.getBetaP()

    def getDetailedStockData(self):
        stock_data = []
        for stock in self.stocks:
            stock_data.append({
                "Stock": stock.symbol,
                "Weight %": self.getWeight(stock)*100,
                "Value $": stock.getAmount(),
                "Beta": stock.getBeta(),
                "Sharpe": stock.getSharpeRatio(),
                "Sortino": stock.getSortinoRatio()
            })
        return pd.DataFrame(stock_data)

    def Summary(self):
        summary = {
            "Portfolio Value": self.getValue(),
            "Portfolio Beta": self.getBetaP(),
            "Portfolio Sharpe": self.getPortfolioSharpe(),
            "Portfolio Sortino": self.getPortfolioSortino(),
            "Portfolio Treynor": self.getTreynorRatio()
        }
        return summary

def main(input_file_path, output_file_path):
    df_stocks = pd.read_excel(input_file_path)

    risk_free_rate = 0.048  
    stocks = []

    for index, row in df_stocks.iterrows():
        stock = Stock(symbol=row['Symbol'], 
                      invested=row['Invested'], 
                      value=row['Value'], 
                      risk_free_rate=risk_free_rate)
        stocks.append(stock)

    portfolio = Portfolio(stocks, risk_free_rate)

    detailed_stock_data = portfolio.getDetailedStockData()
    portfolio_summary = portfolio.Summary()

    summary_df = pd.DataFrame([portfolio_summary])

    with pd.ExcelWriter(output_file_path) as writer:
        detailed_stock_data.to_excel(writer, sheet_name='Detailed Stock Data', index=False)
        summary_df.to_excel(writer, sheet_name='Portfolio Summary', index=False)
    
    return output_file_path

main()
