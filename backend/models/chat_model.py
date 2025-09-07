"""
这是一个问诊模型，模拟中医与病人的问诊过程，并进行诊断。
功能：
- 根据用户输入症状和舌象信息进行问诊
- 支持调用 RAG 检索工具获取中医知识
- 支持调用望诊工具分析舌苔图片
- 返回格式化诊断和调理建议
"""


import asyncio
import requests
from typing import Optional, Dict, List
from backend.config import settings
import httpx
import os
from openai import OpenAI
from backend.RAG.retriever import retrieve
from backend.models.vision_model import analyze_tongue_image
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

client = OpenAI(
    base_url=settings.CHAT_MODEL_LLM_ENDPOINT,
    api_key=settings.DASHSCOPE_API_KEY
)


#----------------------
async def consult_llm(
    question: str,
    tongue_feature: Optional[str],
    chat_history: Optional[List[Dict[str, str]]],
):


    # RAG 检索 -----------------
    retrieved_docs = retrieve(question, k=3)
    rag_context = ""
    if retrieved_docs:
        rag_context = "以下为知识库检索到的相关信息，仅供参考：\n"
        for i, doc in enumerate(retrieved_docs, 1):
            rag_context += f"{i}.{doc['title']} - {doc['content']}\n"
        rag_context += "\n请在回答时结合病人说的症状进行辨证，不要生硬照搬。"


    if tongue_feature:
        curr_prompt = f"舌苔特征: {tongue_feature}。\n症状特征: {question}"
    else:
        curr_prompt = f"症状特征: {question}"

    one_shot_example = [
        {"role":"user", "content":"你叫什么名字？"},
        {"role":"assistant","content":"您好，我是您的专属私人中医智能体-qwen, 很高兴为您服务！请问您需要什么帮助？"},
        {
            "role":"user",
            "content":"我的舌苔发白，有齿痕，有口臭，是什么原因，应该如何调理？"
        },
        {
            "role":"assistant",
            "content":"您好，我是您的专属私人中医智能体，很高兴为您服务！\n\n舌苔发白、有齿痕且伴随口臭, 多与脾胃功能失调、水湿内停密切相关。\n 一、核心成因:\n[脾胃虚弱，水湿内停]: 脾主运化水湿”，若长期饮食不规律（如过食生冷、油腻）、劳累过度或情绪焦虑，会导致脾胃功能减弱，无法正常运化体内水湿，湿气积聚在体内，就会出现舌苔白腻、舌边有齿痕（舌体胖大受牙齿挤压所致）。\n[湿浊内阻，胃气上逆]: 脾胃虚弱会导致 “胃气不降反升”，同时内停的湿浊会与胃中浊气结合，向上熏蒸口腔，进而出现口臭；若湿浊长期滞留，还可能伴随腹胀、大便黏腻不成形、肢体沉重等症状。\n\n\n 二、针对性调理方式\n1. 饮食调理：忌 “湿” 养 “脾” \n<宜吃的食物>（健脾祛湿、助胃气）: \n主食: 小米、山药、茯苓、芡实、炒薏米（生薏米性寒，炒后更适合健脾，避免加重脾胃寒）；\n蔬菜: 南瓜、冬瓜、炒扁豆、胡萝卜；\n其他: 生姜（少量，可温胃散寒，改善湿浊）、陈皮（泡水喝，理气和胃，减少浊气上逆）。\n\n<忌吃的食物>（避免加重湿浊和脾胃负担）:\n生冷食物: 冰饮、雪糕、生鱼片等生冷食物,会进一步损伤脾阳，加重水湿; \n油腻/甜腻食物：油炸食品、蛋糕、奶茶、辣椒、花椒等，易滋生痰湿，加重舌苔白腻和口臭；\n辛辣刺激食物: 辣椒、花椒等，可能刺激胃黏膜，导致胃气上逆更明显。\n\n2. 生活习惯调整：减少 “湿邪” 滋生\n[规律作息，避免熬夜]：熬夜会耗伤脾气，影响脾胃运化功能，建议 23 点前入睡;\n[适度运动，促进祛湿]：选择温和的运动（如快走、瑜伽、八段锦），每周 3-4 次，每次 30 分钟左右，可通过出汗帮助排出体内湿气，同时增强脾胃动力; \n[注意口腔卫生]：饭后及时漱口，早晚刷牙（可轻刷舌苔，避免舌苔过厚堆积浊气），减少口腔局部细菌滋生，辅助改善口臭。\n\n3. 中医干预：辅助健脾祛湿\n<食疗方>:\n山药茯苓粥: 山药 30g、茯苓 15g、大米 50g, 煮成粥，每日 1 次，健脾祛湿效果温和；\n陈皮生姜水: 陈皮 5g、生姜 2 片，开水冲泡代茶饮，可温胃理气，缓解湿浊上逆引起的口臭。\n\n<穴位按摩>\n足三里穴(外膝眼下 3 寸，胫骨外侧 1 横指处）：每次按揉 3-5 分钟，每日 2 次，能健脾和胃、增强脾胃运化能力；\n丰隆穴(外膝眼下 8 寸，胫骨外侧 2 横指处）：每次按揉 3 分钟，每日 1 次，可化痰祛湿，改善湿浊内阻。 \n\n就医提示: 若调理 1-2 周后，舌苔白腻、齿痕、口臭无明显改善，或伴随腹胀、大便稀溏、乏力加重，建议及时到正规中医院就诊，由中医师辨证后开具中药调理，避免延误病情。\n"
        }
    ]

    system_message = {
        "role":"system",
        "content":"你是一名专业的中医医生，你的名字叫私人中医智能体，你的任务是对病人进行问诊，病人可能会问你一下其他与问诊无关的问题，你也都可以回答，并引导病人说出病情。病人会告诉你各种情况，比如病症、病史，你需要根须病人告诉你的信息来具体分析，并进行诊断。诊断时，如果你可以得到舌象信息，你需要结合舌象信息来分析，如果没有舌象信息，就直接根据病人告诉你的信息来分析。但必需从中医的视角来分析，并告诉病人核心原因、针对性调理方式（包含饮食调理，宜吃的食物、忌吃的食物；生活习惯调整；中医干预治疗方式）。必需按照以上格式要求来完成，以下为你与病人对话的格式示例：\n"
        }


    messages = [system_message]
    messages.extend(one_shot_example)
    
    if chat_history:
        messages.extend(chat_history)

    user_message = f"{curr_prompt}\n\n{rag_context}" if rag_context else curr_prompt
    messages.append({"role":"user","content":user_message})

#-------------------------------------------------------------------------------------------------------------
    #调用模型
    # if stream:
    #     # 使用 MCP 流式返回
    #     async for chunk in client.chat.completions.stream(
    #         model=settings.CHAT_MODEL_NAME,
    #         messages=messages,
    #         extra_body={"stream": True}
    #     ):
    #         yield chunk.choices[0].delta.content
    # else:
    #     completion = client.chat.completions.create(
    #         model=settings.CHAT_MODEL_NAME,
    #         messages=messages,
    #     )
    #     yield completion.choices[0].message.content


    try:
        completion = client.chat.completions.create(
            model=settings.CHAT_MODEL_NAME,
            messages=messages,
        )

        #get answer
        answer = completion.choices[0].message.content
        if not answer:
            return "抱歉～ 问诊文字模型没有返回结果，请稍后再试!"
            
        return answer

    except Exception as e:
        return f"问诊文字模型调用失败，错误: {str(e)}"
    