from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

app = FastAPI()

@app.get("/api/reports/top-products", response_model=list[schemas.TopProduct])
def top_products(limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    products = crud.get_top_products(db, limit)
    return products

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    activity = crud.get_channel_activity(db, channel_name)
    return activity

@app.get("/api/search/messages", response_model=list[schemas.Message])
def search_messages(query: str, db: Session = Depends(get_db)):
    messages = crud.search_messages(db, query)
    return messages
