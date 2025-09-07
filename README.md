

# 私人中医智能体 (TCM AI Agent)

> 一个多模态智能体，结合问诊和望诊功能，为用户提供专业中医健康咨询。智能体采用 **RAG（Retrieval-Augmented Generation）** 增强问诊能力，并通过 **MCP 协议** 高效管理模型调用，结合 NVIDIA GPU 加速多模态处理。  

---

## 项目概述

私人中医智能体是一款基于 AI 的专业中医健康问诊系统，能够模拟真实中医门诊场景，进行问诊及望诊，让用户足不出户就享受私人中医专家门诊服务。

1. **文本问诊**：用户输入症状信息，智能体结合多轮对话历史和中医知识库，提供精准的问诊建议。  
2. **舌诊（望诊）分析**：用户上传舌头图片，系统通过视觉模型分析舌质、舌苔特征，提供专业中医诊断参考。  
3. **多模态融合**：文本与图像信息融合，形成更完整的问诊上下文，提高智能体回答的专业性和准确性。  

---

## 系统架构

```

\[前端] React / TailwindCSS / shadcn UI
|
v
\[后端] FastAPI + MCP 协议 + Python Async + SQLAlchemy
|
v
\[模型] Qwen-Turbo / Qwen-VL-Max (问诊 & 望诊)
|
v
\[NVIDIA GPU] 多模态计算加速
|
v
\[数据库] SQLite (存储会话历史与图片路径)

````

### 前端
- 使用 **React** 搭建响应式聊天界面  
- **TailwindCSS** + **shadcn UI** 美化界面，渐变色、长方形对话框、现代化按钮设计  
- 支持用户文本输入和图片上传功能  

### 后端
- **FastAPI** 提供高性能异步接口  
- **MCP 协议** 管理问诊模型与望诊模型的调用，支持多模型协作  
- **RAG (Retrieval-Augmented Generation)**：结合知识库增强问诊模型回答的准确性  
- **SQLAlchemy** 管理会话与消息存储  

---

## 模型说明

### 问诊模型
- 名称：`qwen-turbo` 或 `qwen-plus`  
- 功能：处理用户文本输入，结合历史对话和知识库提供专业问诊答案  
- 百炼：https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.2621657bz7lNzC&tab=model#/model-market/detail/qwen3?modelGroup=qwen3

### 望诊模型
- 名称：`qwen-vl-max`  
- 功能：处理用户舌头图片，通过视觉分析提取舌质、舌苔特征  
- 使用 **Few-shot Learning** 提供示例参考，提高多模态诊断准确性  
- 百炼：https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.2621657bz7lNzC&tab=model#/model-market/detail/qwen-vl-max?modelGroup=qwen-vl-max
- few-shot图片及知识来源:《中医诊法图谱》，作者是顾亦楷先生和费兆馥先生，上海中医学院出版社出版。来源链接:http://www.zhongyijinnang.com/?p=17037
---

## NVIDIA 技术应用

系统在模型推理中充分利用 NVIDIA 硬件与软件技术，包括：

- **GPU 加速**：NVIDIA GPU 提升多模态模型推理速度  
- **CUDA / cuDNN / TensorRT**：优化深度学习模型执行  
- **NVIDIA AI SDK** 支持高性能异步推理  

这些技术确保问诊和望诊模型在百炼平台上运行，并实现低延迟响应。


---

## 创新点

1. **多模态智能体**：文本问诊 + 视觉望诊结合，提升中医诊断智能化水平  
2. **RAG 集成**：结合中医知识库，实现增强生成能力，保证回答专业性  
3. **MCP 协议**：高效管理多模型调用，支持异步交互和流式输出  
4. **Few-shot 视觉/文本学习**：望诊/问诊模型使用示例图片及示例文本进行few-shot学习，提高诊断准确性
5. **高性能部署**：利用 NVIDIA GPU 和百炼平台，实现模型推理加速  


---

## 功能实现

- 用户文本问诊  
- 用户舌头图片望诊分析  
- 多轮对话记忆（历史记录存储于数据库）  
- 问诊 + 望诊结果融合  
- 支持前端文件上传和富文本显示  

---

## 技术栈与依赖

- **前端**：
  - React 18  
  - TailwindCSS 3.x  
  - shadcn/ui 组件库  
- **后端**：
  - Python 3.10+  
  - FastAPI  
  - SQLAlchemy  
  - MCP 协议管理多模型  
  - httpx / asyncio  
- **模型**：
  - Qwen-Turbo / Qwen-Plus（文本问诊）  
  - Qwen-VL-Max（视觉望诊）  
- **其他**：
  - NVIDIA GPU + CUDA/cuDNN/TensorRT  
  - 百炼平台 API Key  

---

## 项目安装与启动

### 1. 克隆项目
```bash
git clone <repo_url>
cd TCM_Agent
````

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. 配置环境变量

```可在bash/.env文件进行配置：
export DASHSCOPE_API_KEY="your_api_key"
export CHAT_MODEL_LLM_ENDPOINT="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### 4. 启动后端

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 5. 启动前端

```bash
cd frontend
python3 -m http.server 3000
# 打开浏览器访问 http://localhost:3000
```


## 作者

* **开发者**: 李新蕊Summer
* **GitHub**: \https://github.com/releerr/Traditional_Chinese_Medicine_Agent.git
* **联系邮箱**: \releehi@163.com

---

## License

本项目遵循 MIT License。

```
