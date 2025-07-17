from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "fct_messages"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String)
    message_date = Column(String)
    message_text = Column(String)
    message_length = Column(Integer)
    has_image = Column(String)

class TopProduct(Base):
    __tablename__ = "top_products_view"  # Example view/table
    product = Column(String, primary_key=True)
    count = Column(Integer)

class ChannelActivity(Base):
    __tablename__ = "channel_activity_view"  # Example view/table
    channel_name = Column(String, primary_key=True)
    activity = Column(Integer)
