import os
from dotenv import load_dotenv

#读取.env
load_dotenv()

class Settings:
    def __init__(self):
        self.DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY")
        self.CHAT_MODEL_LLM_ENDPOINT: str = os.getenv("CHAT_MODEL_LLM_ENDPOINT")
        self.DATABASE_URL:str = os.getenv("DATABASE_URL")
        self.FRONTEND_DEV_URL:str = os.getenv("FRONTEND_DEV_URL")

        self.CHAT_MODEL_NAME:str = os.getenv("CHAT_MODEL_NAME")
        self.VISUAL_MODEL_NAME:str = os.getenv("VISUAL_MODEL_NAME")
        
        self.RISK_NOTICE:str = os.getenv("RISK_NOTICE")



#instance化
settings = Settings()
