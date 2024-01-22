from fastapi import APIRouter
from api.api_v2.endpoints import clients, forms, profile_summary, wallets, transactions, classification, exchanges

api_router = APIRouter()
api_router.include_router(clients.router, prefix="/client", tags=["Client"])
api_router.include_router(profile_summary.router, prefix="/profileSummary", tags=["Profile Summary"])
api_router.include_router(wallets.router, prefix="/wallets", tags=["Wallets"])
# api_router.include_router(exchanges.router, prefix="/exchanges", tags=["Exchanges"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(classification.router, prefix="/classification", tags=["Classification"])
api_router.include_router(forms.router, prefix="/forms", tags=["Forms"])