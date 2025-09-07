from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

#一次完整的问诊回话
class Conversation(Base):
    __tablename__ = "conversations" 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())

    #one conversations has multi-message down below
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer,ForeignKey("conversations.id"),index=True)
    role = Column(String) #user or assistance
    content = Column(Text)
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())


    # every messages all belong to the same conversation
    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )
