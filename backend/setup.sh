#!/bin/bash

# ---------------------------
# 自动化环境安装脚本
# ---------------------------

ENV_NAME="tcm_agent"
PYTHON_VERSION="3.10"

echo "===== Step 1: 创建 Conda 环境 ====="
conda create -y -n $ENV_NAME python=$PYTHON_VERSION

echo "===== Step 2: 激活 Conda 环境 ====="
conda activate $ENV_NAME

echo "===== Step 3: 安装 FAISS CPU 版 ====="
conda install -y -c pytorch faiss-cpu

echo "===== Step 4: 升级 pip ====="
python -m pip install --upgrade pip

echo "===== Step 5: 安装 pip 依赖 ====="
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "没有找到 requirements.txt 文件，请确认路径正确"
fi

echo "===== Step 6: 安装完成 ====="
echo "Ok - Conda 环境 $ENV_NAME 已准备好"
echo "要启动后端，请执行："
echo "conda activate $ENV_NAME"
echo "uvicorn backend.main:app --reload"
