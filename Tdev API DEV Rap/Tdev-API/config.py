import json
import os

class Settings:
	def __init__(self):
		with open("envName.json", "r") as json_file:
				envName = json.load(json_file)
		self.env = os.getenv(envName["appApiEnvironment"])
		self.env = self.env.lower()
		configData = self.activate_env()
		self.loggerConnStr = os.getenv(configData["apiLoggerConnStr"])
		self.API_V1_STR = configData["API_V1_STR"]
		self.API_V2_STR = configData["API_V2_STR"]
		self.aud = configData["aud"]
		self.iss = configData["iss"]
		self.cdbAccessKey = os.getenv(configData["cdbEnvAccessKey"])
		self.saAccessKey = os.getenv(configData["saEnvAccessKey"])
		
		self.origins = configData["origins"]
		self.allow_credentials = configData["allow_credentials"]
		self.allow_methods = configData["allow_methods"]
		self.allow_headers = configData["allow_headers"]
		self.jwks_uri=configData["jwks_uri"]
		
	def activate_env(self):
		if self.env == "dev":
			with open("configDataDev.json", "r") as json_file:
				configData = json.load(json_file)
		elif self.env == "uat":
			with open("configDataUat.json", "r") as json_file:
				configData = json.load(json_file)
		elif self.env == "stg":
			with open("configDataStg.json", "r") as json_file:
				configData = json.load(json_file)
		elif self.env == "prod":
			with open("configDataProd.json", "r") as json_file:
				configData = json.load(json_file)
		return configData
		

settings = Settings()