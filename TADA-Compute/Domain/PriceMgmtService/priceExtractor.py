from Domain.PriceMgmtService.coinGeckoConfig import config, configMethods
from collections import defaultdict
from calendar import monthrange
import html_to_json
import datetime 
import requests
import time 
import json

from Infrastructure.blobMgmt import blobSet

from LoggerUtils import App_logger

def toUnixTimestamp(timestamp:str):
    d = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%SZ')
    unixtime =  time.mktime(d.timetuple())
    return int(unixtime)

def convert_HTML_to_JSON(data):
    if not isinstance(data, dict):
        App_logger.warning("data is in HTML")
        data_json = html_to_json.convert(data)
    return data_json

def unixtimeToDatetime(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d

class priceExtractor:
    "Data extractor from coingecko API"
    def __init__(self, assert_platform):
        self.assert_platform = assert_platform
        self.priceUrl = config.priceUrl
        self.priceUrl_Byid = config.priceUrl_coinid
        self.native_token_id = config.chainParam[self.assert_platform]

    def coinGeckoAPI_range(self, address, startTime, endTime, maxRetry = 5):
        unixStartTime = toUnixTimestamp(startTime)
        unixEndTime = toUnixTimestamp(endTime)
        url = self.priceUrl.format(self.assert_platform, address, unixStartTime, unixEndTime)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers, timeout=120, verify = False)
            data = json.loads(response.text)
            if not isinstance(data, dict):
                data = convert_HTML_to_JSON(data)
                if len(data["prices"]) > 0:
                    return self.coinGeckoAPI_range(address, startTime, endTime, maxRetry-1)
        except:
            try:
                if maxRetry > 0:
                    time.sleep(5/maxRetry)
                    return self.coinGeckoAPI_range(address, startTime, endTime, maxRetry-1)
                return {"prices": []}
            
            except Exception as err:
                App_logger.warning("Pricing - Timeout while fetching Price within range")
                return {"prices": []}

        return data

    def coinGeckoAPI_range_NativeToken(self, startTime, endTime, maxRetry = 5):
        unixStartTime = toUnixTimestamp(startTime)
        unixEndTime = toUnixTimestamp(endTime)
        url = self.priceUrl_Byid.format(self.native_token_id, unixStartTime, unixEndTime)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers, timeout=120, verify = False)
            data = json.loads(response.text)
            if not isinstance(data, dict):
                data = convert_HTML_to_JSON(data)
                if len(data["prices"]) > 0:
                    return self.coinGeckoAPI_range_NativeToken(startTime, endTime, maxRetry-1)
        except:
            try:
                if maxRetry > 0:
                    time.sleep(5/maxRetry)
                    return self.coinGeckoAPI_range_NativeToken(startTime, endTime, maxRetry-1)
                return {"prices": []}

            except Exception as err:
                App_logger.warning("Pricing - Timeout while fetching Price within range for NativeToken")
                return {"prices": []}

        return data

    def extractDataMonthly(self, token, address, startTime, endTime):
        token = token.lower()
        monthDict = defaultdict(dict)
        # if it is a native token
        if address == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
            data = self.coinGeckoAPI_range_NativeToken(startTime, endTime)
        else:
            data = self.coinGeckoAPI_range(address, startTime, endTime)
        if "prices" not in data.keys():
            if 'error' in data.keys():
                App_logger.error(f'coin: {token}, {address}; {startTime}, {endTime}; Error: {data["error"]}')
            return {'prices': []}
        for unixTime, price in data["prices"]:
            timestamp = unixTime // 1000
            d = unixtimeToDatetime(timestamp)
            d = str(d)
            year, monthName, day, hour = configMethods.getMonthYear(d)
            day = int(day)
            hour = int(hour)
            monthDict[day][hour] = (d, price)
        startDateTime = datetime.datetime.strptime(endTime, config.format)
        if len(monthDict) == monthrange(startDateTime.year, startDateTime.month)[1]:
            self.copyToBlob(token, monthDict, startTime)
        toJsonObj = json.dumps(monthDict, ensure_ascii=False, indent=4)
        return json.loads(toJsonObj)

    def copyToBlob(self, token, data, timeStamp):
        try:
            App_logger.info("Copying Extracted data to Blob")
            year, monthName, day, hour = configMethods.getMonthYear(timeStamp)
            file_name = "-".join([token, year, monthName, "pricing"]) + ".json"
            file_path = "/".join(["coingecko", token, year, monthName, file_name])
            blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
            if not blobClient.exists():
                blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4))
        
        except Exception as err:
            App_logger.info("Pricing - Copying Extracted data to Blob unsuccessful")

if __name__ == "__main__":
    price = priceExtractor('ethereum')
    address = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    start = "2022-10-01T00:00:00Z"
    end = "2022-11-01T00:00:00Z"
    # x = price.coinGeckoAPI_range_Na(address, start, end)
    x = price.coinGeckoAPI_range_NativeToken(start, end)
    print(x)
