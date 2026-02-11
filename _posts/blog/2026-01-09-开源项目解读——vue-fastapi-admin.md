---
layout: post
title: "开源项目解读——vue-fastapi-admin"
date: 2026-01-09
last_modified_at: 2026-01-09
categories: [技术纵横]
tags: [开源]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  一个vue、fastapi的后台管理系统开源项目。
---

### 背景与问题
- 学习fastapi作为web开发的后端框架，项目架构设计，数据库设计，依赖管理等。
- 技术栈：vue3、element-plus、fastapi、sqlalchemy、pydantic等。
- 开源项目地址：[https://github.com/baizunxian/vue-fastapi-admin](https://github.com/baizunxian/vue-fastapi-admin)

### 后端架构
#### 项目结构
项目的核心代码都在APP文件夹下，基本目录结构和功能模块如下
- `app/`： 项目核心代码。
    - apis：包含所有的API路由和处理函数。
    - corelibs：包含核心的库函数，如数据库操作、认证等。
    - db：包含数据库模型定义、数据库迁移脚本等。
    - exceptions：包含自定义的异常类。
    - init：包含项目初始化代码，如数据库初始化、环境变量初始化等。
    - models：包含数据库模型定义。
    - schemas：包含数据验证和序列化的Pydantic模型。
    - services：包含业务逻辑层的代码，如用户服务、角色服务等。
    - utils：包含常用的辅助函数。
- `config/`：配置文件目录，包含数据库配置、环境变量等。
- `env/`：环境变量目录，包含环境变量配置文件。
- `main.py`：项目入口文件，包含应用的初始化和启动代码。
- `requirements.txt`：项目依赖文件，包含项目运行所需的Python库。

#### 内部依赖结构
- 启动入口
项目启动的时候是从main.py启动。 使用python main.py启动项目。
核心代码：
启动服务使用uvicorn，在main.py中定义了一个 `create_app` 函数。   
uvicorn会在启动的时候调用create_app函数，当reload=True时，会在每次修改代码后重新调用create_app函数。


``` python
# ... 导入依赖
@asynccontextmanager
async def start_app(app: FastAPI):
    """ 注册中心 """
    # register_mount(app)  # 挂载静态文件
    redis_pool.init_by_config(config=config)
    init_logger()
    logger.info("日志初始化成功！！!")  # 初始化日志

    yield

    await redis_pool.redis.close()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="vue-fastapi-admin",
                        config=config,
                        description=config.SERVER_DESC,
                        version=config.SERVER_VERSION,
                        lifespan=start_app)
    init_exception(app)  # 注册捕获全局异常
    init_router(app)  # 注册路由
    init_middleware(app)  # 注册请求响应拦截
    init_cors(app)  # 初始化跨域

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=9100, reload=True)
```
而 create_app 函数中是一些列初始化和注册的过程，包括异常处理、路由注册、中间件注册、跨域注册等。

- 异常处理

- 路由注册

- 中间件注册

- 跨域注册

- 数据库mysql

- redis缓存


#### 依赖管理

### 参考