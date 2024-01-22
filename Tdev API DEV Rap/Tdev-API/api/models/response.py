import datetime
from pydantic import BaseModel
from typing import List, Union
from dateutil.parser import parse
from uuid import UUID

class WalletProcessingStatus(BaseModel):
    address: str
    unclassifiedTxs: int
    classifiedTxs: int

class StatusResponse(BaseModel):
    status: str
    message: Union[str, List[WalletProcessingStatus]]

class ClientResponse(BaseModel):
    clientId: UUID
    name: str
    formName: Union[str, None]
    taxId: Union[str, None]
    addrLn1: Union[str, None]
    addrLn2: Union[str, None]
    city: Union[str, None]
    state: Union[str, None]
    zipCode: Union[str, None]
    country: Union[str, None]
    status: Union[StatusResponse, None]

class ManualPostTxsResponse(BaseModel):
    TxnsInserted: int
    TxnsRejected: List[str]

class UnclassifiedTxPutResponse(BaseModel):
    Wallet: str
    TxHash: Union[str, None]
    From: str
    To: str
    Token: str
    TransactionDesc: str
    TxDirection: str
    Amount:str
    Price: str
    TokenList: Union[list, None]
    id: Union[str, None]
    TimeStamp: str
    iconName: Union[str, None]
    assetType: Union[str, None]
    error: Union[StatusResponse, None]
	
class TransactionResponse(BaseModel):
    type: Union[str, None]
    Wallet: str
    TxHash: Union[str, None]
    From: str
    To: Union[str, None]
    Token: str
    TransactionDesc: str
    TxDirection: str
    Amount:str
    Price: Union[str, None]
    TokenList: Union[list, None]
    id: Union[str, None]
    TimeStamp: str
    iconName: Union[str, None]
    assetType: Union[str, None]

class TransactionsByHashResponse(BaseModel):
    TxHash: str
    transactionData: List[TransactionResponse]
    total_count: int
	
class PagedTransactionsByHashResponse(BaseModel):
    data: List[TransactionsByHashResponse]
    start_index: int
    size: int
    total_count: int
	
class PagedTransactionsForKeyResponse(BaseModel):
    transactionData: List[TransactionResponse]
    start_index: int
    size: int
    total_count: int
	
class TransactionsByAssetResponse(BaseModel):
    Asset: str
    total_in: float
    total_out: float
    net_amount: float
    transactionData: List[TransactionResponse]
    total_count: int

class PagedTransactionsByAssetResponse(BaseModel):
    data: List[TransactionsByAssetResponse]
    start_index: int
    size: int
    total_count: int
	
class TaxSummaryResponse(BaseModel):
    fifoTotalTax: float
    lifoTotalTax: float
    hifoTotalTax: float
    mode: str

class ExchangeResponse(BaseModel):
    id: str
    name: str
    apiKey: str
    apiPass: str
    status: Union[str, None]
    assetType: Union[str, None]
    iconName: Union[str, None]
    error: Union[StatusResponse, None]

class ExchangesResponse(BaseModel):
    __root__ : List[ExchangeResponse]
	
class CheckboxResponse(BaseModel):
    optionId: str
    optionValue: bool
	
class SectionCheckboxResponse(BaseModel):
    sectionId: UUID
    checkboxData: List[CheckboxResponse]
	
class ColumnAttrResponse(BaseModel):
    columnId: str
    columnValue: Union[float, str]
    cellId: str
	
class ColumnResponse(BaseModel):
    column: ColumnAttrResponse
	
class RowAttrResponse(BaseModel):
    rowId: str
    columns: List[ColumnResponse]
	
class RowResponse(BaseModel):
    row: RowAttrResponse
	
class SectionTableDataResponse(BaseModel):
    sectionId: UUID
    tableData: List[RowResponse]
    total_count: int
	
class RowAltResponse(BaseModel):
    rowId: UUID
    columns: List[ColumnAttrResponse]
	
class VersionDataResponse(BaseModel):
    version: str
    fileName: str
    creationDate: str
    pdfstatus: str
	
	
class ClientInfoResponse(BaseModel):
    clientId: UUID
    name: str
    businessStatus: str

class ClientInfoListResponse(BaseModel):
    __root__ : List[ClientInfoResponse]
	
class TaxValuesResponse(BaseModel):
    taxLiability: float
    ltcg : float
    stcg: float
    portfolioValueIn: float
    portfolioValueOut: float
	
class HoldingResponse(BaseModel):
    name: str
    amount: float
    totalValue: float
    direction : str
    iconName: str

class HoldingsResponse(BaseModel):
    __root__ : List[HoldingResponse]

	
class DiagramResponse(BaseModel):
    name: str
    size: int

class UserPreferencesResponse(BaseModel):
    diagrams: List[DiagramResponse]  
	
class WalletResponse(BaseModel):
    address: str
    status: Union[str, None]
    chain: str
    iconName: Union[str, None]
    error: Union[StatusResponse, None]

class WalletsResponse(BaseModel):
    __root__ : List[WalletResponse]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]

class AddAccessListResponse(BaseModel):
    nonAddedUsers: List[str]
    addedUsers: List[str]

class ClientUserResponse(BaseModel):
    emailId: str
    isCreator: bool

class ClientUserListResponse(BaseModel):
    __root__: List[ClientUserResponse]

class ManualCsvResponse(BaseModel):
    type: str
    id: str
    Blockchain: Union[str,None]
    Asset: Union[str,None]
    TxHash: str
    Wallet: str
    AssetPlatform: Union[str,None]
    TimeStamp: Union[str,None]
    From: str
    To: str
    Token: Union[str,None]
    Amount: Union[str,None]
    TxDirection:str
    TransactionDesc: Union[str,None]
    Price: Union[str,None]
	# This function detect any datetime format and convert it to "%Y-%m-%dT%H:%M:%SZ"
    def detectAndCovertDatetimeFormat(self, TimeStamp:str):
        datetime_obj = parse(TimeStamp)
        return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    def to_dict(self):
        return {
            'Blockchain': self.Blockchain,
            'Asset': self.Asset,
            'TxHash': self.TxHash.lower(),
            'Wallet': self.Wallet.lower(),
            'AssetPlatform': self.AssetPlatform.lower() if self.AssetPlatform else None,
            'TimeStamp': datetime.datetime.strptime(self.detectAndCovertDatetimeFormat(self.TimeStamp),"%Y-%m-%dT%H:%M:%SZ"),
            'From': self.From.lower(),
            'To': self.To.lower(),
            'Token': self.Token,
            'Amount': self.Amount,
            'TxDirection':self.TxDirection.upper(),
            'TransactionDesc': self.TransactionDesc,
            'Price': self.Price
        }

class ManualGetTxsResponse(BaseModel):
    __root__ : List[ManualCsvResponse]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]