---
layout: post
title:  "fastapi中的StreamingResponse"
date:   2026-03-30
last_modified_at: 2026-03-30
categories: [代码片段]
tags: [code]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  fastapi中的StreamingResponse，用于实现流式响应。
---

## 功能和问题
- 功能描述：
在ai开发中，需要流式返回的场景，可以使用StreamingResponse来实现。
他的用法简单，只要返回一个可迭代对象，就可以实现流式响应。


## 代码片段展示
在router中，使用StreamingResponse来实现流式响应。
``` python
@router.post("/chat")
def chat():
    return StreamingResponse(
        stream_message(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
```
重点是要返回一个可迭代对象，例如generator函数，当我们在大模型交互中，可以使用类似的stream的api调用大模型的接口
``` python
def stream_message():
    for n in range(10):
        time.sleep(1)
        yield f"message {n}"
```


## 前端接收方式
方式一：EventSource  
原生 SSE 接收方式，自动重连、使用简单，但只支持 GET 且无法自定义请求头。
``` js
const sse = new EventSource("/chat")
sse.onopen = () => {
  console.log("connected")
}
sse.onmessage = (event) => {
  console.log(event.data)
}
sse.onerror = () => {
  sse.close()
}
```

方式二：Fetch API  
适合需要 POST、自定义 header 的场景，需要自己解析 SSE 的 data 行。
``` js
const response = await fetch("/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "hi" })
})
const reader = response.body.getReader()
const decoder = new TextDecoder("utf-8")
let buffer = ""
while (true) {
  const { value, done } = await reader.read()
  if (done) break
  buffer += decoder.decode(value, { stream: true })
  const parts = buffer.split("\n\n")
  buffer = parts.pop() || ""
  for (const part of parts) {
    const line = part.split("\n").find((item) => item.startsWith("data:"))
    if (line) {
      const data = line.replace(/^data:\s*/, "")
      console.log(data)
    }
  }
}
```

方式三：fetch-event-source  
第三方库封装 SSE，支持 POST、自定义 header、自动重连，使用前需安装依赖。
``` js
import { fetchEventSource } from "@microsoft/fetch-event-source"

await fetchEventSource("/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "hi" }),
  onmessage(event) {
    console.log(event.data)
  },
  onerror(err) {
    throw err
  }
})
```


## 总结
