from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routers import chat_routerMCP
import os

app = FastAPI(
    title = "TCM AI Assistance",
    description = "我是您的私人中医智能体，您有任何问题都可以问我。诊断仅供辅助参考。",
    version = "1.0"
    )



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    # allow_origins=[settings.FRONTEND_DEV_URL],
    # allow_methods=["GET","POST"],
    # allow_headers=["Authorization", "Content-Type"]
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


#测试接口 - 后端是否启动
@app.get("/")
def root():
    return {"message":"TCM is running !"}

#测试接口 - 读取配置是否成功
@app.get("/config")
def get_config():
    return{
        "chat_model":settings.CHAT_MODEL_NAME,
        "visual_model":settings.VISUAL_MODEL_NAME,
        "risk_notice":settings.RISK_NOTICE
    }


#注册路由，让后续的接口都挂载在对应路由
app.include_router(chat_routerMCP.router)

