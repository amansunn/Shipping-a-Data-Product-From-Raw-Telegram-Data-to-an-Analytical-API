from sqlalchemy.orm import Session
from models import Message, TopProduct, ChannelActivity

# Example queries, adjust for your actual dbt models/views

def get_top_products(db: Session, limit: int):
    return db.query(TopProduct).order_by(TopProduct.count.desc()).limit(limit).all()

def get_channel_activity(db: Session, channel_name: str):
    return db.query(ChannelActivity).filter(ChannelActivity.channel_name == channel_name).first()

def search_messages(db: Session, query: str):
    return db.query(Message).filter(Message.message_text.ilike(f"%{query}%")).all()
