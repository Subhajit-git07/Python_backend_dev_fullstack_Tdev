
class settings:
    # pageSize of Covalent API call for each blockchain
    pageSize = {
        "1": 1000, # Ethereum
        "43114": 500, # Avalanche
        "default": 100
    }
    maxContentSize = 300
    maxValidationTry = 5
    maxFailedPageTry = 3


class config(settings):
    @staticmethod
    def get_api_page_size(chainID: str):
        if chainID in config.pageSize.keys():
            return config.pageSize[chainID]
        else:
            return config.pageSize["default"]