


import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import quantstats as qs

portfolio= input('Enter the Ticker of the stocks in your portfolio as they appear in Yahoo finance, along with the weights, like this " AAPL:0.5, LSEG.L:0.5" : ')
portfolio = portfolio.split(',')
for i in portfolio:
    i=i.upper().split(':')

class Stock():
    def __init__(self, symbol, weight, risk_free_rate):
        self.symbol = symbol
        self.RF = float(risk_free_rate)
        self.weight= weight
        self.data = None
    
    def getTicker(self):
        self.stock = yf.Ticker(self.symbol)
        return self.stock


    def get_data(self, start_date, end_date):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        self.data = yf.download(self.symbol, start=start_date, end=end_date, interval='1d', ignore_tz=True)
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
        sortino = self.getExcessReturns().mean() / self.getExcessReturns()[self.getExcessReturns() < 0].std() * np.sqrt(252)
        return sortino  

    def getTreynorRatio(self):
        treynor = self.getTotalReturn() / self.getBeta()
        return treynor  

    def getInformationRatio(self, benchmark):
        info = (self.getReturns() - benchmark.getReturns()).mean() / (self.getReturns() - benchmark.getReturns()).std() * np.sqrt(252)
        return info  

class Portfolio():
    def __init__(self, stocks, risk_free_rate):
        self.stocks = stocks
        self.data = None
        self.RF = risk_free_rate
    
    def getExpectedReturn(self):
        expectedReturn = 0
        for stock in self.stocks:
            expectedReturn += stock.getTotalReturn() * stock.weight
        return expectedReturn
    
    def getVolatility(self):
        returnsMatrix=[]
        weightsMatrix=[]
        for stock in self.stocks:
            returnsMatrix.append(stock.getReturns())
            weightsMatrix.append(stock.weight)
        returnsMatrix = pd.concat(returnsMatrix, axis=1)
        returnsMatrix=returnsMatrix.dropna()
        returnsMatrix=np.array(returnsMatrix)
        weightsMatrix=np.array(weightsMatrix)
        volatility = np.sqrt(np.dot(weightsMatrix.T, np.dot(np.cov(returnsMatrix), weightsMatrix))) * np.sqrt(252)

        return volatility
    
    def getPortfolioSharpe(self):
        sharpe = (self.getExpectedReturn() - self.RF) / self.getVolatility()
        return sharpe
    

for i in range(int(len(portfolio))):
    portfolio[i] = Stock(portfolio[i][0], float(portfolio[i][1]), 0.05)
    
portfolio = Portfolio(portfolio, 0.05)