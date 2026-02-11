---
layout: post
title:  "Python中读取环境变量——dotenv"
date:   2026-01-09
last_modified_at: 2026-01-09
categories: [代码片段]
tags: [python]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  python中的环境变量管理（python-dotenv）。
---

## 功能和问题
- 功能描述：读取环境变量  
- 问题描述：在Python中，我们可以使用`os`模块来读取环境变量。但是，当环境变量很多时，手动一个一个读取会比较麻烦。  

- 问题描述：使用dotenv库可以更方便地读取环境变量。



## 代码片段展示
``` py
# .env
# 设置环境变量到配置文件里
BAILIAN_APPKEY="sk-7ba735b69340xxxxxxxx"
BAILIAN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME_DEEPSEEK="deepseek-v3.2"
```

```py
# config.py
from dotenv import load_dotenv
load_dotenv()
import os

# 验证环节变量
def _get_env(key: str, default: any = None, required: bool = False):
    """
    读取默认的环节变量
    如果没有环境变量也没有默认值则报错
    :param key:环境变量名
    :param default:默认值
    :param required:是否必须
    :return:
    """
    value = os.getenv(key, default)
    if required and not value:
        raise ValueError(f"{key} 缺少值")
    return value


global_config = {
    "BAILIAN_APPKEY": _get_env("BAILIAN_APPKEY", required= True),
    "BAILIAN_BASE_URL": _get_env("BAILIAN_BASE_URL", required= True),
    "MODEL_NAME_DEEPSEEK": _get_env("MODEL_NAME_DEEPSEEK", required= True),
}

```

``` python
# llm.py
from langchain_openai import ChatOpenAI
from config import global_config

llm = ChatOpenAI(
    model_name=global_config["MODEL_NAME_DEEPSEEK"],
    api_key=global_config["BAILIAN_APPKEY"],
    base_url=global_config["BAILIAN_BASE_URL"]
)

result = llm.invoke("hello")
print(result.content)

```


## 总结

