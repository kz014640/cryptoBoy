from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 10
		self.indicators = BotIndicators()
		self.totalProfit = 0.0
		self.minRSI = 30
		self.maxRSI = 70
		self.minMomentum = 103	
		self.maxMomentum = 97	

	def tick(self,candlestick):
		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		
		#self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

		#self.output.log("Total Profit: "+str(self.totalProfit)) 
		return self.totalProfit

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))
			elif(self.indicators.RSI(self.prices,15) <= self.minRSI):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))
			elif(self.indicators.momentum(self.prices,15) >= self.minMomentum):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))

		for trade in openTrades:
			if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
				trade.close(self.currentPrice)
			elif(self.indicators.RSI(self.prices,15) >= self.maxRSI):
				trade.close(self.currentPrice)
			elif(self.indicators.momentum(self.prices,15) <= self.maxMomentum):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
			if(vars(trade)["tradeProfit"]):
				self.totalProfit = float(vars(trade)["tradeProfit"]) + self.totalProfit