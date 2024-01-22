import calendar

from Config import EnvSettings

class config:
	coinListUrl = EnvSettings.coinListUrl
	priceUrl = EnvSettings.priceUrl
	priceUrl_coinid = EnvSettings.priceUrl_coinid
	format ='%Y-%m-%dT%H:%M:%SZ'
	commonFormat = '%Y-%m-%d %H:%M:%S'
	chainParam = {
		# Based on CoinGecko APIs, AssertPlatform : NativeToken
		"ethereum": "ethereum",
		"avalanche": "avalanche-2",
		"ronin" : "ronin"
	}

class configMethods:
	
	@staticmethod
	def getMonthYear(timeStamp: str):
		month = timeStamp[5:7]
		monthName = calendar.month_abbr[int(month)].upper()
		year = timeStamp[0:4]
		day = timeStamp[8:10]
		hour = timeStamp[11:13]
		return year, monthName, day, hour

	@staticmethod
	def getMonthYearStr(timeStamp: str):
		year, month = timeStamp.split('T')[0].split('-')[:2]
		return year, month