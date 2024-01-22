from pydantic import BaseModel, constr, Extra
from typing import List, Union, Optional
from uuid import UUID
import datetime
from dateutil.parser import parse

class ClientRequest(BaseModel):
    clientId: UUID
    name: constr(min_length=1, max_length=200, strict=True)
    formName: constr(min_length=0, max_length=30, strict=True)
    taxId: constr(min_length=0, max_length=10, strict=True)
    addrLn1: constr(min_length=0, max_length=30, strict=True)
    addrLn2: constr(min_length=0, max_length=30, strict=True)
    city: constr(min_length=0, max_length=30, strict=True)
    state: constr(min_length=0, max_length=30, strict=True)
    zipCode: constr(min_length=0, max_length=9, strict=True)
    country: constr(min_length=0, max_length=30, strict=True)

    class Config:
        extra = Extra.forbid
	
class classificationStatusRequest(BaseModel):
    status: str
    message: str
    
class TransactionRequest(BaseModel):
    Wallet: constr(max_length=50, strict=True)
    TxHash: constr(max_length=150, strict=True)
    From: constr(max_length=50, strict=True)
    To: constr(max_length=50, strict=True)
    Token: constr(max_length=30, strict=True)
    TransactionDesc: constr(max_length=150, strict=True)
    TxDirection: constr(max_length=30, strict=True)
    Amount:constr(max_length=30, strict=True)
    Price: constr(max_length=30, strict=True)
    TokenList: Union[list, None]
    id: constr(max_length=30, strict=True)
    TimeStamp: constr(max_length=30, strict=True)
	
class ExchangeInRequest(BaseModel):
    name: str
    apiKey: str
    apiPass: str

    class Config:
        extra = Extra.forbid

class UserAccessStringRequest(BaseModel):
    user: constr(max_length=200, strict=True)
    def to_dict(self):
        return {
            'user' : self.user
        }
    
    class Config:
        extra = Extra.forbid

class UserAccessListRequest(BaseModel):
    __root__ : List[UserAccessStringRequest]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
    
    class Config:
        extra = Extra.forbid


class UserRemoveAccessRequest(BaseModel):
    user: constr(max_length=200, strict=True)
    def to_dict(self):
        return {
            'user' : self.user
        }

    class Config:
        extra = Extra.forbid
        

class ColumnAttrRqequest(BaseModel):
    columnId: constr(max_length=50, strict=True)
    columnValue: Union[float, str]
    cellId: str

    class Config:
        extra = Extra.forbid

class ColumnRequest(BaseModel):
    column: ColumnAttrRqequest

    class Config:
        extra = Extra.forbid

class RowAttrRequest(BaseModel):
    rowId: UUID
    columns: List[ColumnRequest]

class RowRequest(BaseModel):
    row: RowAttrRequest

    class Config:
        extra = Extra.forbid
	
class CheckboxRequest(BaseModel):
    optionId: UUID
    optionValue: bool

    class Config:
        extra = Extra.forbid

class SectionRequest(BaseModel):
    sectionId: UUID
    checkboxData: List[CheckboxRequest]
    tableData: List[RowRequest]
	
class SectionsRequest(BaseModel):
    sections: List[SectionRequest]

class DiagramRequest(BaseModel):
    name: constr(max_length=50, strict=True)
    size: int

    class Config:
        extra = Extra.forbid

class UserPreferencesRequest(BaseModel):
    diagrams: List[DiagramRequest]  
	
class WalletRequest(BaseModel):
    address: constr(max_length=50, strict=True)
    chain: constr(max_length=15, strict=True)
    def to_dict(self):
        return {
            'address': self.address.lower(),
            'chain': self.chain,
        }
    
    class Config:
        extra = Extra.forbid

class WalletsRequest(BaseModel):
    __root__ : List[WalletRequest]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
		
class ManualCsvRequest(BaseModel):
    class Config:
        extra = Extra.forbid
    Blockchain: constr(max_length=30, strict=True)
    Asset: constr(max_length=50, strict=True)
    TxHash: constr(max_length=150, strict=True)
    Wallet: constr(max_length=50, strict=True)
    # AssetPlatform: constr(max_length=30, strict=True)
    TimeStamp: constr(max_length=30, strict=True)
    From: constr(max_length=50, strict=True)
    To: constr(max_length=50, strict=True)
    Token: constr(max_length=30, strict=True)
    Amount: constr(max_length=30, strict=True)
    TxDirection: constr(max_length=30, strict=True)
    TransactionDesc: constr(max_length=150, strict=True)
    Price: constr(max_length=30, strict=True)
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
        

class ManualUploadsRequest(BaseModel):
    __root__ : List[ManualCsvRequest]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]