---
layout: post
title: "sqlachemy专题"
date: 2026-02-20
last_modified_at: 2026-02-20
categories: [
  技术纵横
  ]
tags: [python]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  sqlachemy是一个python的ORM库， 可以用来操作数据库。
---

### 背景与问题


### 用法用例
代码如下：
如何连接数据库创建表及字段
#### 连接数据库 建表
``` py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

mysql_connection_string = "mysql+pymysql://root:123456@localhost:3306/test"
engine = create_engine(mysql_connection_string)

Base = declarative_base()

class Building(Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

Base.metadata.create_all(engine)

```

#### 数据库的CRUD操作
``` py
from sqlalchemy.orm import sessionmaker
from sc1 import myengine, Building

# 创建会话
sessionmaker = sessionmaker(bind=myengine)
session = sessionmaker()

# crud操作
# 创建 操作
# building = Building(name="building1")
# session.add(building)
# session.commit()

# 查询  操作
building = session.query(Building).all()
for x in building:
    print(x.id, x.name)
```

#### 表映射关系

#### 高级查询

#### 事物处理

### 参考