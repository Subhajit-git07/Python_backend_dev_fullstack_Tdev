from pydantic import BaseModel
from typing import List, Union
from uuid import UUID

class WalletProcessingStatusDomain(BaseModel):
    address: str
    unclassifiedTxs: int
    classifiedTxs: int

class StatusResponseDomain(BaseModel):
    status: str
    message: Union[str, List[WalletProcessingStatusDomain]]

class ClientResponseDomain(BaseModel):
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
    status : Union[StatusResponseDomain, None]

class UnclassifiedTxPutResponseDomain(BaseModel):
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
    error: Union[StatusResponseDomain, None]

class TaxSummaryResponseDomain(BaseModel):
    fifoTotalTax: float
    lifoTotalTax: float
    hifoTotalTax: float
    mode: str

class AddAccessListResponseDomain(BaseModel):
    nonAddedUsers: List[str]
    addedUsers: List[str]

class WalletResponseDomain(BaseModel):
    address: str
    status: Union[str, None]
    chain: str
    iconName: Union[str, None]
    error: Union[StatusResponseDomain, None]

class WalletsResponseDomain(BaseModel):
    __root__ : List[WalletResponseDomain]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]

class ClientUserResponseDomain(BaseModel):
    emailId: str
    isCreator: bool

class ClientUserListResponseDomain(BaseModel):
    __root__: List[ClientUserResponseDomain]