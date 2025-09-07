"""
用于中医中的望诊，分析用户上传的舌头照片, 提取舌头特征，通过望诊模型进行分析，并输出格式化结果。

few-shot图片及知识来源:《中医诊法图谱》，作者是顾亦楷先生和费兆馥先生，上海中医学院出版社出版。
- 来源链接:http://www.zhongyijinnang.com/?p=17037
"""


import httpx
import json
from backend.config import settings
import asyncio
from openai import OpenAI
import os
import base64


client = OpenAI(
    api_key=settings.DASHSCOPE_API_KEY,
    base_url=settings.CHAT_MODEL_LLM_ENDPOINT
)

BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BACKEND_DIR, "data") 
FEW_SHOT_PATH = os.path.join(DATA_DIR, "vision_model_few_shot.json")
if not os.path.exists(FEW_SHOT_PATH):
    raise FileNotFoundError(f"Few-shot 文件未找到，请确认路径是否正确: {FEW_SHOT_PATH}")

#望诊模型调用
async def analyze_tongue_image(image_path:str) -> str:
    
    with open(FEW_SHOT_PATH, 'r', encoding="utf-8") as f:
        few_shot_examples = json.load(f)

    messages = [
        {"role": "system", "content": "你是一名专业的中医望诊专家，你能够专业的分析病人的舌苔图片并描述舌质和舌苔特征。如下述这些例子所示："}
    ]

    for ex in few_shot_examples:
        img_path = os.path.join(DATA_DIR, ex["image_path"])
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Few-shot 图片未找到: {img_path}")
        with open(img_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        messages.append({
            "role": "user",
            "content": "请分析这张舌苔图片并描述舌质、舌苔特征。",
            "image": img_base64  
        })
        messages.append({
            "role": "assistant",
            "content": ex["description"]
        })

    with open(image_path, 'rb') as user_img:
        user_img_base64 = base64.b64encode(user_img.read()).decode("utf-8")
    messages.append({
        "role": "user",
        "content": "请分析这张舌苔图片并描述舌质、舌苔特征。",
        "image": user_img_base64
    })


# 调用模型
    try:
        completion = client.chat.completions.create(
            model=settings.VISUAL_MODEL_NAME,
            messages=messages,
        )

        # 打印原始返回，方便调试
        print("completion 原始返回:", completion)

        # 提取回答
        answer = "[望诊视觉模型未返回结果]"
        if hasattr(completion, "choices") and len(completion.choices) > 0:
            choice = completion.choices[0]  # Choice 对象
            if hasattr(choice, "message") and choice.message:
                answer = choice.message.content or answer

        return answer

    except Exception as e:
        return f"望诊视觉模型调用失败，错误: {str(e)}"