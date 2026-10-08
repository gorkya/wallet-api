from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import InsufficientFundsError, WalletNotFoundError
from app.routers import wallets

app = FastAPI(title="Wallet API")
app.include_router(wallets.router)


@app.exception_handler(WalletNotFoundError)
async def wallet_not_found_handler(request: Request, exc: WalletNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Wallet not found"},
    )


@app.exception_handler(InsufficientFundsError)
async def insufficient_funds_handler(
    request: Request, exc: InsufficientFundsError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Insufficient funds"},
    )
