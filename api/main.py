from fastapi import FastAPI
from app import scraper

app = FastAPI()


@app.get("/books")
async def get_all_books():
    return {"data": scraper.get_all_books()}