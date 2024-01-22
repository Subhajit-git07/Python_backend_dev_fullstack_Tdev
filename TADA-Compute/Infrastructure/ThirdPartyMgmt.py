import os

from Config import EnvSettings

class ThirdPartySettings():
    def __init__(self):
        self.CovalentKey = os.getenv(EnvSettings.CovalentAccessKey)
        self.CoinGeckoKey = os.getenv(EnvSettings.CoinGeckoAccessKey)

ThirdPartySet = ThirdPartySettings()