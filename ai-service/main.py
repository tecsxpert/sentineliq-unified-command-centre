from fastapi import FastAPI
from routes import report

app = FastAPI()

app.include_router(report.router)