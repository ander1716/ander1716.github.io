---
layout: post
title: "Llamalndex"
date: 2026-02-15
last_modified_at: 2026-02-15
categories: [
  技术纵横
  ]
tags: [LLamaIndex]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  LLamaIndex介绍和用法。
---

### 背景与问题
LLamaIndex是一个开源的大模型上下文增强框架，注重于数据连接和加载、索引构建、访自然语言查询、数据存储、工作流编排、智能体（Agent）开发、评估模块以及与多种LLM和向量数据库的集成。  

使用场景：
- Rag问答
- 聊天机器人
- 结构化数据抽取 
- 多模态应用等

更专注 RAG，检索、索引、文档处理更强，上手更轻量

### 核心概念
- Document：你的原始数据（txt、pdf、md、csv…）
- Node：文档切分后的小块
- Index：把 Node 变成向量 / 索引，方便快速查找
- Retriever：从 Index 里检索相关内容
- Query Engine：检索 + 大模型生成回答



### 一个简单的agent创建
``` py
from llama_index.core.agent.workflow import FunctionAgent

llm_client = OpenAILike(
    model=os.getenv("DASHSCOPE_MODEL_QWEN3_MAX"),
    api_base=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    is_chat_model=True,
    context_window=32768,
    is_function_calling_model=True,
)

agent = FunctionAgent(
    tools=[getWeather],
    llm=llm_client,
    system_prompt="You are a helpful assistant",
)

```


### rag
在llama_index中可以自动切片文档，也可以手动定义切片规则。
``` py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader("docs").load_data()

auto_index = VectorStoreIndex.from_documents(documents)
auto_query_engine = auto_index.as_query_engine()
auto_answer = auto_query_engine.query("总结这些文档的主题")
print(auto_answer)

manual_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=128)
Settings.node_parser = manual_splitter
manual_index = VectorStoreIndex.from_documents(documents)
manual_query_engine = manual_index.as_query_engine()
manual_answer = manual_query_engine.query("提取关键要点")
print(manual_answer)
```


### api学习
#### Settings
Settings可以提前设置好LLM模型和向量化模型，这样后面调用的时候就默认使用这个模型，否则默认是OpenAi的模型
``` py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
import os
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels
)
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels

APIKEY= os.getenv("DASHSCOPE_API_KEY")

Settings.embed_model = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V1,
    api_key=APIKEY
)

Settings.llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX,
    api_key=APIKEY
)

```  

#### Document
document对象，所有读取到的文档都是document对象，也提供了Document方法来将文本转位Document对象。使用`Document(text="text")`将文本转位Document对象
```py
# Document对象是来自llama_index.core模块的Document类
from llama_index.core import Document
text_list = [
    "This is a test document.",
    "This is another test document.",
    "This is a third test document.",
]
docs = [Document(text=text) for text in text_list]
print(docs)
```

#### SimpleDirectoryReader
读取文件目录下的文件称为document对象,如案例是将docs目录下的文件称为Document对象，一个txt文件是一个Document对象，返回的是list
``` py
from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader('docs').load_data()
print(documents)
```



### 参考
