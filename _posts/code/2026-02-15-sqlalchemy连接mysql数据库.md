---
layout: post
title:  "SQLAlchemy连接MySQL数据库"
date:   2026-02-15
last_modified_at: 2026-02-15
categories: [代码片段]
tags: [code]
cover: https://qiniu.zhuyucun.cn/uploads/1764853276621_kn1jl7.jpg
excerpt: >
  SQLAlchemy是一个Python的SQL工具包和对象关系映射（ORM）库，它提供了一个高级的抽象层，用于与数据库进行交互。
---

## 功能和问题
- 功能描述：sqlalchemy连接MySQL数据库
- 问题描述：用于fastapi项目中连接MySQL数据库

## 代码片段展示

```py
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from contextlib import contextmanager

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)  # 加唯一约束
    email = Column(String(255), nullable=False, unique=True)  # 加唯一约束
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_tables(self):
        """建表（单独的方法，手动调用）"""
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """提供自动关闭的 session 上下文"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_user(self, username, email, password, avatar):
        """添加用户（带异常处理）"""
        with self.session_scope() as session:
            new_user = User(
                username=username,
                email=email,
                password=password,
                avatar=avatar
            )
            session.add(new_user)
            # 自动 commit

    def get_user_by_id(self, user_id):
        """根据 ID 查询用户"""
        with self.session_scope() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_all_users(self):
        """查询所有用户，并在会话内部打印信息"""
        with self.session_scope() as session:
            users = session.query(User).all()
            return users

    def get_users_by_status(self, status):
        """按状态查询用户"""
        with self.session_scope() as session:
            return session.query(User).filter(User.status == status).all()


# 使用示例
if __name__ == "__main__":
    # 初始化
    db_manager = DatabaseManager("mysql+pymysql://root:123456@127.0.0.1/test")

    # 建表（只需执行一次）
    # db_manager.create_tables()

    # 添加用户
    try:
        db_manager.add_user(
            username="李四",
            email="lisi@example.com",  # ✅ 正确的邮箱格式
            password="123456",
            avatar="https://example.com/avatar.png"
        )
        print("用户添加成功")
    except Exception as e:
        print(f"添加失败: {e}")

    # 查询用户
    db_manager.get_all_users()

```


## fastApi集成sqlalchemy
1、环境准备
安装 `fastapi` `sqlalchemy` `pymysql` `asyncmy` `uvicorn` `pydantic-settings` 等必要的库
2、配置文件
config.py
``` py
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """数据库配置设置"""
    
    # 数据库基本信息
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "test"
    
    # 连接池配置
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # 编码配置
    DB_CHARSET: str = "utf8mb4"
    
    # SQLALCHEMY配置
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    @property
    def database_url(self) -> str:
        """生成同步数据库URL"""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?charset={self.DB_CHARSET}"
        )
    
    @property
    def async_database_url(self) -> str:
        """生成异步数据库URL"""
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?charset={self.DB_CHARSET}"
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = DatabaseSettings()
```
3、数据库连接管理
创建connection.py, 定义DatabaseManager，用于管理数据库连接和会话，创建 init_sync_engine 和 init_async_engine 两种初始化引擎    sessionmaker 被用来创建同步和异步的会话工厂
``` py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator, AsyncGenerator
import logging

from .config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 创建基类
Base = declarative_base()

class DatabaseManager:
    """数据库管理器 - 生产级别封装"""
    
    def __init__(self):
        self._sync_engine = None
        self._async_engine = None
        self._sync_session_local = None
        self._async_session_local = None
        
    def init_sync_engine(self):
        """初始化同步数据库引擎"""
        if self._sync_engine is None:
            self._sync_engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_timeout=settings.DB_POOL_TIMEOUT,
                pool_recycle=settings.DB_POOL_RECYCLE,
                echo=settings.SQLALCHEMY_ECHO,
                pool_pre_ping=True,  # 连接前检测
            )
            logger.info("同步数据库引擎初始化完成")
        
        if self._sync_session_local is None:
            self._sync_session_local = sessionmaker(
                bind=self._sync_engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
            
    def init_async_engine(self):
        """初始化异步数据库引擎"""
        if self._async_engine is None:
            self._async_engine = create_async_engine(
                settings.async_database_url,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_timeout=settings.DB_POOL_TIMEOUT,
                pool_recycle=settings.DB_POOL_RECYCLE,
                echo=settings.SQLALCHEMY_ECHO,
                pool_pre_ping=True,
            )
            logger.info("异步数据库引擎初始化完成")
            
        if self._async_session_local is None:
            self._async_session_local = sessionmaker(
                bind=self._async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
    
    @property
    def sync_engine(self):
        """获取同步引擎"""
        if self._sync_engine is None:
            self.init_sync_engine()
        return self._sync_engine
    
    @property
    def async_engine(self):
        """获取异步引擎"""
        if self._async_engine is None:
            self.init_async_engine()
        return self._async_engine
    
    @property
    def sync_session_local(self):
        """获取同步会话工厂"""
        if self._sync_session_local is None:
            self.init_sync_engine()
        return self._sync_session_local
    
    @property
    def async_session_local(self):
        """获取异步会话工厂"""
        if self._async_session_local is None:
            self.init_async_engine()
        return self._async_session_local
    
    @contextmanager
    def get_sync_db(self) -> Generator:
        """获取同步数据库会话上下文管理器"""
        db = self.sync_session_local()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            db.close()
    
    async def get_async_db(self) -> AsyncGenerator[AsyncSession, None]:
        """获取异步数据库会话"""
        async with self.async_session_local() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"异步数据库操作失败: {e}")
                raise
    
    def create_tables(self):
        """创建所有表"""
        try:
            Base.metadata.create_all(bind=self.sync_engine)
            logger.info("数据库表创建完成")
        except Exception as e:
            logger.error(f"创建数据库表失败: {e}")
            raise
    
    def drop_tables(self):
        """删除所有表"""
        try:
            Base.metadata.drop_all(bind=self.sync_engine)
            logger.info("数据库表删除成功")
        except Exception as e:
            logger.error(f"删除数据库表失败: {e}")
            raise
    
    async def close_connections(self):
        """关闭所有数据库连接"""
        if self._async_engine:
            await self._async_engine.dispose()
        if self._sync_engine:
            self._sync_engine.dispose()
        logger.info("数据库连接已关闭")


# 全局数据库管理器实例
db_manager = DatabaseManager()

```

4、在fastapi中调用  
在启动的时候调用数据库初始化，

``` py
# main.py

# Lifespan 事件处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    try:
        # 应用启动时初始化数据库连接
        db_manager.init_sync_engine()
        db_manager.init_async_engine()
        db_manager.create_tables()
        logger.info("数据库连接初始化成功")
        yield  # 应用运行期间保持连接
    finally:
        # 应用关闭时清理资源
        await db_manager.close_connections()
        logger.info("数据库连接已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="FastAPI Production Project",
    description="生产级别的FastAPI项目，包含完整的数据库集成",
    version="1.0.0",
    lifespan=lifespan
)

```

``` py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator, AsyncGenerator
import logging

from .connection import db_manager

logger = logging.getLogger(__name__)


def get_sync_db() -> Generator[Session, None, None]:
    """
    同步数据库会话依赖
    
    使用示例:
    @app.get("/users/")
    def get_users(db: Session = Depends(get_sync_db)):
        users = db.query(User).all()
        return users
    """
    with db_manager.get_sync_db() as db:
        try:
            yield db
        except Exception as e:
            logger.error(f"同步数据库会话错误: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="数据库操作失败"
            )


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    异步数据库会话依赖
    
    使用示例:
    @app.get("/users/")
    async def get_users(db: AsyncSession = Depends(get_async_db)):
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    """
    async with db_manager.get_async_db() as db:
        try:
            yield db
        except Exception as e:
            logger.error(f"异步数据库会话错误: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="数据库操作失败"
            )


class DatabaseDependencies:
    """数据库依赖集合类"""
    
    @staticmethod
    def sync_db():
        """同步数据库依赖"""
        return Depends(get_sync_db)
    
    @staticmethod
    def async_db():
        """异步数据库依赖"""
        return Depends(get_async_db)


# 便捷别名
SyncDB = DatabaseDependencies.sync_db()
AsyncDB = DatabaseDependencies.async_db()

```

坑点bcrypt和passlib的版本要对应：
    "bcrypt==3.2.0",
    "passlib==1.7.4",

## 总结

app/
├── database/
│   ├── config.py          # 数据库配置
│   ├── connection.py      # 数据库连接管理
│   └── dependencies.py    # 依赖注入
├── models/                # SQLAlchemy 模型
├── schemas/               # Pydantic Schema
├── crud/                  # 数据库操作逻辑
└── main.py                # FastAPI 应用入口


