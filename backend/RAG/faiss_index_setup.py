import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

#-----------------TODO---------------------------------------------------------------------

docs = [
    {"title": "失眠调理", "content": "中医认为失眠主要与心肝脾有关，可通过针灸、按摩和饮食调理。"},
    {"title": "胃胀饮食", "content": "胃胀的人应避免油腻辛辣食物，多吃易消化的食物。"},
    {"title": "咳嗽调理", "content": "风寒咳嗽可用生姜红糖水，注意保暖，多喝温水。"},
    {"title": "月经不调", "content": "月经不调多与肝脾气血有关，可通过穴位按摩和中药调理。"}
]

#---------------------------------------------------------------------------------------------------

INDEX_DIR = "faiss_index"
INDEX_PATH = os.path.join(INDEX_DIR, "TCM_index.faiss")
DOCS_PATH = os.path.join(INDEX_DIR, "TCM_docs.pkl")
MODEL_NAME = "BAAI/bge-small-zh-v1.5" 

def build_and_save_index():
    os.makedirs(INDEX_DIR,exist_ok=True)

    print(f"[1/4] 加载嵌入模型：{MODEL_NAME}")
    embedding_model = SentenceTransformer(MODEL_NAME)

    texts = [doc["content"]for doc in docs] 
    print(f"[2/4] 生成文档向量，共 {len(texts)} 条")
    embeddings = embedding_model.encode(texts, convert_to_numpy=True,normalize_embeddings=True)

    #create faiss index
    d = embeddings.shape[1]
    print(f"[3/4] 构建 FAISS 索引（IndexFlatL2, 维度={d}）")

    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    print(f"[3/4] 构建 FAISS 索引（IndexFlatL2, 维度={d}）")
    #save index and docs
    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)
                
    print("FAISS index created！")
    print(f"   - 索引文件: {INDEX_PATH}")
    print(f"   - 文档文件: {DOCS_PATH}")


if __name__ == "__main__":
    build_and_save_index()