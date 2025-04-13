from pydantic import BaseModel, Field
from datetime import datetime

class OrderDetails(BaseModel):
    accountNumber: str
    ordererCustomer: str
    currency: str
    instrumentName: str
    instrumentIsin: str
    instrumentCurrency: str
    instrumentMarket: str
    orderReference: str
    orderStatus: str
    orderOperationType: str
    orderOperationTypeEnum: str
    orderType: str
    orderDate: datetime
    finishDate: datetime
    shares: int
    limitPrice: float
    grossAmountCurrency: float
    executionDate: datetime
    priceCurrency: float
    executedShares: int
    grossAmountOperationCurrency: float
    tradeCommissions: float
    otherCommissions: float
    exchangeRate: float
    netAmountEUR: float
    netAmountCurrency: float