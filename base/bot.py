import sys, getopt
import time
import pprint

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick
from botTime import BotTime

def main(argv):

	startTime = False
	endTime = False

	try:
		opts, args = getopt.getopt(argv,"hp:c:n:s:e:a:",["period=","currency=","points="])
	except getopt.GetoptError:
		print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
		sys.exit(2)
	print(opts)
	for opt, arg in opts:
		if opt == '-h':
			print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
			sys.exit()
		elif opt in ("-p", "--period"):
			if (int(arg) in [300,900,1800,7200,14400,86400]):
				period = arg
			else:
				print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments'
				sys.exit(2)
		elif opt in ("-c", "--currency"):
			pair = arg
		elif opt in ("-n", "--points"):
			lengthOfMA = int(arg)
		elif opt in ("-s"):
			startTime = arg
		elif opt in ("-e"):
			endTime = arg
		elif opt in ("-a"):
			auto = arg

	if (startTime):
		chart = BotChart("poloniex","BTC_XMR",300,True,startTime,endTime)
		chart2 = BotChart("poloniex","USDT_BTC",300,True,startTime,endTime)
		chart3 = BotChart("poloniex","USDC_BTC",300,True,startTime,endTime)
		chart4 = BotChart("poloniex","BTC_ETH",300,True,startTime,endTime)
		
		strategy = BotStrategy()
		strategy2 = BotStrategy()
		strategy3 = BotStrategy()
		strategy4 = BotStrategy()

		print("start1")
		for candlestick in chart.getPoints():
			total = strategy.tick(candlestick)
		print("Total is: " + str(total))

		print("start2")
		for candlestick in chart2.getPoints():
			total = strategy2.tick(candlestick)
		print("Total is: " + str(total))

		print("start3")
		for candlestick in chart3.getPoints():
			total = strategy3.tick(candlestick)
		print("Total is: " + str(total))

		print("start4")
		for candlestick in chart4.getPoints():
			total = strategy4.tick(candlestick)
		print("Total is: " + str(total))

	elif(auto):
		time = BotTime(10)
		endTime = time.startDate()
		startTime = time.endDate()

		chart = BotChart("poloniex","BTC_XMR",300,True,startTime,endTime)
		chart2 = BotChart("poloniex","USDT_BTC",300,True,startTime,endTime)
		chart3 = BotChart("poloniex","USDC_BTC",300,True,startTime,endTime)
		chart4 = BotChart("poloniex","BTC_ETH",300,True,startTime,endTime)
		
		strategy = BotStrategy()
		strategy2 = BotStrategy()
		strategy3 = BotStrategy()
		strategy4 = BotStrategy()

		print("chart1")
		for candlestick in chart.getPoints():
			total = strategy.tick(candlestick)
		print("Total is: " + str((total*6972.90)))

		print("chart2")
		for candlestick in chart2.getPoints():
			total = strategy2.tick(candlestick)
		print("Total is: " + str((total*0.80)))

		print("chart3")
		for candlestick in chart3.getPoints():
			total = strategy3.tick(candlestick)
		print("Total is: " + str((total*0.80)))

		print("chart4")
		for candlestick in chart4.getPoints():
			total = strategy4.tick(candlestick)
		print("Total is: " + str((total*6972.90)))

	else:
		chart = BotChart("poloniex","BTC_XMR",300,False)
		
		strategy = BotStrategy()

		candlesticks = []
		developingCandlestick = BotCandlestick()

		while True:
			try:
				developingCandlestick.tick(chart.getCurrentPrice())
			except urllib2.URLError:
				time.sleep(int(30))
				developingCandlestick.tick(chart.getCurrentPrice())

			if (developingCandlestick.isClosed()):
				candlesticks.append(developingCandlestick)
				strategy.tick(developingCandlestick)
				developingCandlestick = BotCandlestick()
		
			time.sleep(int(30))

if __name__ == "__main__":
	main(sys.argv[1:])