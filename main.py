from fastapi import FastAPI
from database import create_tables
from contextlib import asynccontextmanager
from routers import users, transactions
import uvicorn


@asynccontextmanager
async def lifespan_events(app: FastAPI):
    await create_tables()

    yield


app = FastAPI(
    title="Wallet APis",
    version="1.0.0",
    lifespan=lifespan_events
)

app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return { "message": "Working" }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)