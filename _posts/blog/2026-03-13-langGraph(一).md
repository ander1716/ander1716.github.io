---
layout: post
title: "langGraph(一)"
date: 2026-03-13
last_modified_at: 2026-03-13
categories: [
  技术纵横
  ]
tags: [langGraph]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  这篇文章是关于langGraph的，它是一个用于构建和管理语言模型的框架。
---

### 背景与问题
langchain的langGraph是一个用于构建和管理语言模型的框架。它提供了一种简单而强大的方式来定义和执行语言模型的任务。
- 前者用于简单的任务，可以链式调用，一次执行完成。
- 后者对复杂任务的处理能力更强，支持循环、条件判断等复杂逻辑。

### 基本概念
1. 节点（Node）：
Graph 中所有节点**共享的数据容器**。
表示一个任务的节点。每个节点都有一个唯一的标识符和一个定义好的任务。  

2. 边（Edge）：
一个**普通 Python 函数**，接收当前 state，返回需要更新的字段。
表示节点之间的依赖关系或执行顺序。每条边都有一个方向，从一个节点指向另一个节点。

3. 状态（State）：  
**连接节点**，定义执行流程。
表示语言模型在执行过程中的中间结果或上下文。状态可以在节点之间传递，用于存储和更新信息。


### 执行流程

``` bash
START → node_a → node_b → node_c → END
        ↑读写State  ↑读写State  ↑读写State
```

### hello world
```python
"""
第 01 节：LangGraph 核心概念 - State、Node、Edge

这是最简单的 LangGraph 程序：
  START → 问候节点 → 大写节点 → END
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. 定义 State（图的共享数据结构）
# ============================================================
class State(TypedDict):
    message: str   # 消息内容
    result: str    # 处理结果


# ============================================================
# 2. 定义 Node（处理函数）
# ============================================================
def greet_node(state: State) -> dict:
    """问候节点：在消息前加上问候语"""
    greeted = f"你好！收到你的消息：{state['message']}"
    print(f"[greet_node] {greeted}")
    return {"result": greeted}


def uppercase_node(state: State) -> dict:
    """大写节点：把 result 中的英文字母转大写"""
    upper = state["result"].upper()
    print(f"[uppercase_node] {upper}")
    return {"result": upper}


# ============================================================
# 3. 构建 Graph（连接节点和边）
# ============================================================
builder = StateGraph(State)

# 添加节点
builder.add_node("greet", greet_node)
builder.add_node("uppercase", uppercase_node)

# 添加边（定义执行顺序）
builder.add_edge(START, "greet")       # 起点 → greet
builder.add_edge("greet", "uppercase") # greet → uppercase
builder.add_edge("uppercase", END)     # uppercase → 终点

# 编译（生成可运行的 graph）
graph = builder.compile()


# ============================================================
# 4. 运行
# ============================================================
if __name__ == "__main__":
    # 传入初始 State
    initial_state = {"message": "hello LangGraph", "result": ""}

    print("=== 开始运行 Graph ===")
    final_state = graph.invoke(initial_state)

    print("\n=== 最终 State ===")
    print(final_state)

```

### 总结使用步骤
1. 定义 State 数据结构，用于存储和传递信息。
2. 实现 Node 函数，定义每个任务的处理逻辑。
3. 使用 StateGraph 构建图，添加节点和边。
4. 编译图，生成可运行的 graph。
5. 传入初始 State，调用 graph.invoke() 执行任务。

### 注意事项
- 每个节点的处理函数必须接收并返回 State 字典。
- 节点之间的边必须定义好方向，从一个节点指向另一个节点。
- 状态（State）是图的共享数据结构，所有节点都可以读写它。
- 节点必须返回一个字典，包含需要更新的字段即可（无须全部返回）
