---
layout: post
title: "langchain核心api"
date: 2026-02-21
last_modified_at: 2026-02-21
categories: [
  技术纵横
  ]
tags: [langchain]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  langchain是一个python的库， 可以用来操作大模型。
---

## 背景与问题
langcain是一个开源的python库，封装了简化大模型操作的api，提供了统一的接口，方便开发者使用。本文主要是记录常用的api及其用法。

## 核心
### 连接大模型的api
- init_chat_model 
- ChatOpenAI
- 各个厂商自己的api
第一种方式是使用init_chat_model初始化大模型，返回一个chat_model对象，国内的模型model_provider默认是openai，需要提供api_key和base_url来区分。
``` py
# 百炼平台大模型链接
llm_client from langchain.chat_models import init_chat_model
= init_chat_model(
    model="qwen3-max-2026-01-23",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

其次遵循openai规范的大模型使用ChatOpenAI这个api可以连接，无需提供给model_provider参数。
``` py
llm_client_ofrom langchain_openai import ChatOpenAI
penai = ChatOpenAI(
    model="qwen3-max-2026-01-23",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```
最后的各个厂商都有自己的api在langchain社区封装的，如：
百炼大模型的
``` py
from langchain_community.chat_models.tongyi import ChatTongyi

llm_dashscope = ChatTongyi(
    model="qwen3-max-2026-01-23",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

```

### agents智能体
智能体是集成了大模型，工具和中间件等组件的一个对象，用于执行任务。
``` py
agent = create_agent(
    model = llm_client,
    tools = [get_weather, get_location],
    system_prompt="你是一个生活助手，耐心回答用户问题",
    middleware=[
        logger,
        # 摘要中间键
        SummarizationMiddleware(
            model=llm_client,
            keep=("messages", 20),
            trigger=("tokens", 4000),
        )
    ]
)
```

### PromptTemplate

``` py
from langchain_core.prompts import PromptTemplate

# 定义一个包含变量的模板
template = "你是一名{role}工程师，请帮我设计{feature}的单元测试用例"
prompt = PromptTemplate(
    input_variables=["role", "feature"],
    template=template
)

# 格式化生成最终的提示字符串
formatted_prompt = prompt.format(role="资深测试", feature="条件覆盖")
print(formatted_prompt)
# 输出: 你是一名资深测试工程师，请帮我设计条件覆盖的单元测试用例

# 或者直接使用from_template
# prompt = PromptTemplate.from_template("你是一名{role}, 现在请{feature}")
# format_prompt = prompt.format(role="历史专家", feature="介绍刘备")
# print(format_prompt)
```
### ChatPromptTemplate
用于多轮对话 有from_messages和 from_template两个方法，  
from_messages接收一个消息列表，每个消息是一个元组，第一个元素是消息的角色，第二个元素是消息的内容。  
from_template接收的是一个模板字符串，模板字符串中可以包含变量，变量用大括号{}括起来。  
``` py
from langchain_core.prompts import ChatPromptTemplate
from model import llm_client
prompt = ChatPromptTemplate.from_messages( [
    ("system", "你是一个{role}"),
    ("human", "请帮我{feature}")
])
res = llm_client.invoke(prompt.format(role="历史专家", feature="介绍秦始皇"))

print(res)

```

### DocumentLoaders
文档加载器用于加载文档，将文档转换为langchain的文档对象。

```py
from langchain_community.document_loaders import TextLoader

# 加载文本 转为document对象
loader = TextLoader("../docs/deepseek-intro.txt")
document = loader.load()
print(document)
```
langchain_community还提供了很多了loader 如 PyPDFLoader、Docx2txtLoader、WebBaseLoader等


### 文档分块
langchain里的切割器有哪些？

- CharacterTextSplitter
    按字符切割文档，默认是按换行符切割。

- RecursiveCharacterTextSplitter
    递归按字符切割文档，默认是按换行符切割。

- TokenTextSplitter
    按token切割文档，token切分不需要大模型参与，而是使用了本地的tokenizer，只要设置encoding_name即可
    如：
``` py
from langchain.text_splitter import TokenTextSplitter
text_splitter = TokenTextSplitter(encoding_name="cl100k_base")
```
# 这些编码器都是本地的，不需要 API
TokenTextSplitter(encoding_name="cl100k_base")      # GPT-3.5/4 的 tokenizer
TokenTextSplitter(encoding_name="p50k_base")        # GPT-3 的 tokenizer
TokenTextSplitter(encoding_name="r50k_base")        # GPT-2 的 tokenizer
TokenTextSplitter(model_name="gpt-3.5-turbo")       # 自动选择 cl100k_base

- MarkdownTextSplitter
    按markdown语法切割文档

其他还有：
``` py
    "CharacterTextSplitter",
    "ElementType",
    "ExperimentalMarkdownSyntaxTextSplitter",
    "HTMLHeaderTextSplitter",
    "HTMLSectionSplitter",
    "HTMLSemanticPreservingSplitter",
    "HeaderType",
    "JSFrameworkTextSplitter",
    "KonlpyTextSplitter",
    "Language",
    "LatexTextSplitter",
    "LineType",
    "MarkdownHeaderTextSplitter",
    "MarkdownTextSplitter",
    "NLTKTextSplitter",
    "PythonCodeTextSplitter",
    "RecursiveCharacterTextSplitter",
    "RecursiveJsonSplitter",
    "SentenceTransformersTokenTextSplitter",
    "SpacyTextSplitter",
    "TextSplitter",
    "TokenTextSplitter",
    "Tokenizer",
    "split_text_on_tokens",
```

### 参考