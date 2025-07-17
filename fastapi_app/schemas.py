from pydantic import BaseModel

class Message(BaseModel):
    id: int
    channel_id: str
    message_date: str
    message_text: str
    message_length: int
    has_image: str

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    activity: int
