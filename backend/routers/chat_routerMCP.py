from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from backend.database.db_connection import get_db
from backend.database.db_models import Conversation, Message
from backend.RAG.retriever import retrieve
from backend.models.vision_model import analyze_tongue_image
from backend.config import settings
from backend.models.chat_model import consult_llm
# from fastMCP import MCPServer, MCPRequest
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.prompts import ChatPromptTemplate
from fastapi.responses import StreamingResponse
from fastapi import Request


import os
from uuid import uuid4
import asyncio
import base64
import json

router = APIRouter(prefix="/chat",tags=["chat"])

UPLOAD_DIR = "user_uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)



#fastMCP request -----------------------------------------------------
@router.post("/send")
async def chat_stream(
    user_input: Optional[str] = Form(None), 
    user_id: int = Form(1), 
    db: Session = Depends(get_db),
    tongue_image: Optional[UploadFile] = File(None)
):

    # data = await request.json()
    # user_input = data.get("message", "")
    # user_id = data.get("user_id", 1)

    
    #if there are conversation before,add conversation in-----------------------------------------------------
    conversation = db.query(Conversation).filter(Conversation.user_id==user_id).first()
    if conversation:
        messages = conversation.messages
        chat_history = [
            {"role":"user" if m.role == "user" else "assistant",
             "content":m.content if isinstance(m.content, str) else json.dumps(m.content)}
            for m in messages
        ]
    else:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        chat_history=[]

    #if there are image, then analyze image ------------------------------------------------------------
    tongue_feature = None 
    image_path = None 

    if tongue_image:
        filename = f'{uuid4().hex}_{tongue_image.filename}'
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath,'wb') as f:
            f.write(await tongue_image.read())
        image_path = filepath
        try:
            tongue_feature = await analyze_tongue_image(filepath) #调用望诊模型
        except Exception as e:
            print(f"[WARNING] analyze_tongue_image 调用失败: {e}")
            tongue_feature = "" 

    
    if not user_input and not tongue_feature:
        prompt = "您好，我是您的专属私人中医智能体，如果您有哪里不舒服都可以向我咨询。愿您健康平安！"
    else:
        prompt = user_input



    try:
        answer = await consult_llm(
            question=prompt,
            tongue_feature=tongue_feature or "",
            chat_history=chat_history
        )
    except Exception as e:
        answer = f"[MODEL ERROR] 模型调用失败: {str(e)}"

    


#------------------------------------------------------------------------------------------------------------------------
    #save to database
    user_message = Message(
        conversation_id = conversation.id,
        role = "user",
        content = user_input,
        image_path=image_path
    )

    assistance_message = Message(
        conversation_id = conversation.id,
        role = "assistant",
        content = answer
    )

    db.add_all([user_message,assistance_message])
    db.commit()

    return {
        "user_input":user_input,
        "answer":answer,
        "history_length":len(chat_history) + 2 #加上本次回话
    }

