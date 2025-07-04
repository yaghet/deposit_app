import uvicorn
from fastapi import FastAPI

from app.api.v1.routes.wallet import router as wallet_router

app = FastAPI(title="Wallet API")

app.include_router(wallet_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
