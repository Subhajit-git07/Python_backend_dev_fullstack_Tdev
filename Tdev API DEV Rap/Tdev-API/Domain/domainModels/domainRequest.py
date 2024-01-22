import datetime
from pydantic import BaseModel, constr, Extra
from typing import List, Union
from uuid import UUID
from dateutil.parser import parse

class ClientRequestDomain(BaseModel):
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
	
class classificationStatusRequestDomain(BaseModel):
    status: str
    message: str
	
class TransactionRequestDomain(BaseModel):
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
		
class ExchangeInRequestDomain(BaseModel):
    name: str
    apiKey: str
    apiPass: str
	
class ColumnAttrRqequestDomain(BaseModel):
    columnId: str
    columnValue: Union[float, str]
    cellId: str

class ColumnRequestDomain(BaseModel):
    column: ColumnAttrRqequestDomain

class RowAttrRequestDomain(BaseModel):
    rowId: UUID
    columns: List[ColumnRequestDomain]

class RowRequestDomain(BaseModel):
    row: RowAttrRequestDomain
	
class CheckboxRequestDomain(BaseModel):
    optionId: UUID
    optionValue: bool

class SectionRequestDomain(BaseModel):
    sectionId: UUID
    checkboxData: List[CheckboxRequestDomain]
    tableData: List[RowRequestDomain]
	
class SectionsRequestDomain(BaseModel):
    sections: List[SectionRequestDomain]

class DiagramRequestDomain(BaseModel):
    name: str
    size: int

class UserPreferencesRequestDomain(BaseModel):
    diagrams: List[DiagramRequestDomain]  
	
class WalletRequestDomain(BaseModel):
    address: str
    chain: Union[str, None]
    def to_dict(self):
        return {
            'address': self.address.lower(),
            'chain': self.chain
        }

class WalletsRequestDomain(BaseModel):
    __root__ : List[WalletRequestDomain]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
		
		
# class WalletOutRequestDomain(BaseModel):
#     address: str
#     status: Union[str, None]
#     chain: str
#     iconName: Union[str, None]
#     error: Union[classificationStatusRequestDomain, None]

# class WalletsOutRequestDomain(BaseModel):
#     __root__ : List[WalletOutRequestDomain]
#     def __iter__(self):
#         return iter(self.__root__)
#     def __getitem__(self, item):
#         return self.__root__[item]
		
class ExchangeOutRequestDomain(BaseModel):
    id: str
    name: str
    apiKey: str
    apiPass: str
    status: Union[str, None]
    assetType: Union[str, None]
    iconName: Union[str, None]
    error: Union[classificationStatusRequestDomain, None]

class ExchangesOutRequestDomain(BaseModel):
   __root__ : List[ExchangeOutRequestDomain]
   
class TaxValuesRequestDomain(BaseModel):
    taxLiability: float
    ltcg : float
    stcg: float
    portfolioValueIn: float
    portfolioValueOut: float
	
# class TransactionOutRequestDomain(BaseModel):
#     Wallet: str
#     TxHash: Union[str, None]
#     From: str
#     To: str
#     Token: str
#     TransactionDesc: str
#     TxDirection: str
#     Amount:str
#     Price: str
#     TokenList: Union[list, None]
#     id: Union[str, None]
#     TimeStamp: str
#     iconName: Union[str, None]
#     assetType: Union[str, None]
#     error: Union[classificationStatusRequestDomain, None]
	
	
class ManualCsvRequestDomain(BaseModel):
	Blockchain: Union[str,None]
	Asset: Union[str,None]
	TxHash: str
	Wallet: str
	# AssetPlatform: Union[str,None]
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
			# 'AssetPlatform': self.AssetPlatform.lower() if self.AssetPlatform else None,
			'TimeStamp': datetime.datetime.strptime(self.detectAndCovertDatetimeFormat(self.TimeStamp),"%Y-%m-%dT%H:%M:%SZ"),
			'From': self.From.lower(),
			'To': self.To.lower(),
			'Token': self.Token,
			'Amount': self.Amount,
			'TxDirection':self.TxDirection.upper(),
			'TransactionDesc': self.TransactionDesc,
			'Price': self.Price
		}

class ManualUploadsRequestDomain(BaseModel):
    __root__ : List[ManualCsvRequestDomain]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
		
class AddWalletRequestDomain(BaseModel):
    chainid: str
    clientId: str
    wallet: str
	
	
class UserAccessStringRequestDomain(BaseModel):
    user: constr(max_length=200, strict=True)
    def to_dict(self):
        return {
            'user' : self.user
        }
    
    class Config:
        extra = Extra.forbid

class UserAccessListRequestDomain(BaseModel):
    __root__ : List[UserAccessStringRequestDomain]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
    
    class Config:
        extra = Extra.forbid