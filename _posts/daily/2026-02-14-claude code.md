---
layout: post
title:  "claude code"
date:   2026-02-14
last_modified_at: 2026-02-14
categories: [日常]
tags: [daily]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
---

## 摘要
- 本文用于记录Claude code工具的使用

## 安装和升级
``` bash
# mac系统上安装 
curl -fsSL https://claude.ai/install.sh | bash
# 使用npm pnpm安装 （目前我的安装方式）
pnpm add -g @anthropic-ai/claude-code
# ... ...

# 更新的时候要使用相应的命令更新要最新版本
pnpm update -g @anthropic-ai/claude-code

# 查看安装版本
claude --version

# 查看安装位置
which claude
```

## 配置
### 进入claude code
``` bash
# 进入工作目录  然后执行
claude

# 选择 Yes, proceed
────────────────────────────────────────────────────────────────────────────────
 Do you trust the files in this folder?

 /Users/zhuyucun/Documents/learning/python-test/claude-code-test

 Claude Code may read, write, or execute files contained in this directory.
 This can pose security risks, so only use files from trusted sources.

 Learn more ( https://docs.claude.com/s/claude-code-security )

 ❯ 1. Yes, proceed
   2. No, exit

 Enter to confirm · Esc to exit
```

## 使用


## claude code 原理
`Bash is All You Need` 他的核心就是一个循环的bash执行，一个工具+一个循环=一个智能体  
核心步骤：
提示用户必须使用bash命令
- 用户发起一个message，发送给LLM
- 大模型响应需要的bash命令
- 执行bash命令
- 返回执行结果继续给LLM
- 直到返回`stop_reason != "tool_use"`  

``` python
# 最简单的一个demo
from openai import OpenAI
import os
from dotenv import load_dotenv
import subprocess

# 加载环境变量
load_dotenv()

# ------------------- 阿里云百炼配置 -------------------
API_KEY = os.getenv("BAILIAN_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen3-max-2026-01-23"  # 通义千问最强模型，支持工具调用

# 初始化客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 系统提示
SYSTEM = "你是一个可以执行终端命令的智能助手，必须使用工具调用执行命令，不要直接回答"

# 工具定义（百炼/OpenAI 格式）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "执行终端命令",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的命令"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

# 执行命令函数
def run_bash(command):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=20
        )
        return f"输出:\n{result.stdout}\n错误:\n{result.stderr}"
    except Exception as e:
        return f"执行失败: {str(e)}"

# ------------------- 核心 Agent 循环（和你原版逻辑完全一致） -------------------
def agent_loop(query):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": query}
    ]

    while True:
        # 调用百炼 API
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        answer = response.choices[0].message
        messages.append(answer.model_dump())  # 保存AI回复
        print("\n🤖 AI回复:", answer.content)

        # 如果没有工具调用 → 结束
        if not answer.tool_calls:
            return

        # 执行工具调用
        tool_results = []
        for tool in answer.tool_calls:
            cmd = tool.function.arguments
            # 解析 JSON 命令
            import json
            cmd = json.loads(cmd)["command"]
            print(f"\n🔧 执行命令: {cmd}")
            output = run_bash(cmd)

            tool_results.append({
                "role": "tool",
                "tool_call_id": tool.id,
                "content": output
            })

        # 把结果返回给AI
        messages.extend(tool_results)

# ------------------- 测试 -------------------
if __name__ == "__main__":
    user_query = """
      Create a file called hello.py that prints "Hello, World!"
      List all Python files in this directory
      What is the current git branch?
      Create a directory called test_output and write 3 files in it
    """
    print(f"🧑 用户: {user_query}")
    agent_loop(user_query)

# 运行结果如下  python s01_agent_loop.py
# 🧑 用户: 
# Create a file called hello.py that prints "Hello, World!"
# List all Python files in this directory
# What is the current git branch?
# Create a directory called test_output and write 3 files in it

# 🤖 AI回复: 

# 🔧 执行命令: echo 'print("Hello, World!")' > hello.py

# 🔧 执行命令: ls *.py

# 🔧 执行命令: git branch --show-current

# 🔧 执行命令: mkdir -p test_output && echo "File 1 content" > test_output/file1.txt && echo "File 2 content" > test_output/file2.txt && echo "File 3 content" > test_output/file3.txt

# 🤖 AI回复: 1. 文件 `hello.py` 已成功创建，内容为打印 "Hello, World!"。
# 2. 当前目录中的 Python 文件包括：`hello.py` 和 `s01_agent_loop.py`。
# 3. 当前目录不是一个 Git 仓库，因此无法获取 Git 分支信息。
# 4. 目录 `test_output` 已成功创建，并在其中写入了三个文件：`file1.txt`、`file2.txt` 和 `file3.txt`。

```


## 参考
- [Claude Code官方](https://code.claude.com/docs/en/quickstart)
- [智谱Ai接入到Claude code](https://docs.bigmodel.cn/cn/coding-plan/tool/claude)
- [Claude code npm包](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [learn claude code](https://learn.shareai.run/zh/)
