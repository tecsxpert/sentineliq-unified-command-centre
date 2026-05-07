from fastapi import FastAPI
from routes import query, categorise

app = FastAPI()

app.include_router(query.router)
app.include_router(categorise.router)