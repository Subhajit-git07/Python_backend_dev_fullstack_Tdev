import json
import os
	
class Settings:
    def __init__(self):

        with open("envName.json", "r")as json_file:
            envName = json.load(json_file)
        
        # Environment & Connection strings
        self.env = os.getenv(envName["AppComputeEnvironment"])
        ConfigData = self.Active_Environment(self.env)
        self.logger_string = os.getenv(ConfigData["ApplicationLoggerKey"])
        self.aud = ConfigData["aud"]
        self.iss = ConfigData["iss"]
        self.cdbAccessKey = ConfigData["cdbEnvAccessKey"]
        self.CovalentAccessKey = ConfigData["covalentEnvAccessKey"]
        self.CoinGeckoAccessKey = ConfigData["coinGeckoEnvAccessKey"]
        self.saAccessKey = ConfigData["saEnvAccessKey"]

        # Third pary URL's
        self.coinListUrl = ConfigData["coinListUrl"]
        self.priceUrl = ConfigData["priceUrl"]
        self.priceUrl_coinid = ConfigData["priceUrl_coinid"]
        self.transactionUrl = ConfigData["transactionUrl"]
        self.OnetransactionUrl = ConfigData["OnetransactionUrl"]
        self.BalancesUrl = ConfigData["BalancesUrl"]
        self.validateWallet = ConfigData["validateWallet"]
        self.api_url = ConfigData["api_url"]
        self.api_exchange_info = ConfigData["api_exchange_info"]

    def Active_Environment(self, env:str):
        if env.lower() == "prod":
            with open("ConfigDataPROD.json", "r") as prod_file:
                configData = json.load(prod_file)
        elif env.lower() == "dev":
            with open("ConfigDataDEV.json", "r") as dev_file:
                configData = json.load(dev_file)
        elif env.lower() == "qa":
            with open("ConfigDataQA.json", "r") as qa_file:
                configData = json.load(qa_file)
        elif env.lower() == "uat":
            with open("ConfigDataUAT.json", "r") as uat_file:
                configData = json.load(uat_file)
        return configData

EnvSettings = Settings()