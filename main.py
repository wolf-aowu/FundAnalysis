from app.routers.root import root_router
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.configs.cors_config import origins
from app.utils.config import get_config
from app.utils.database import get_async_database_url
from app.servers.middlewares import ProcessTimeMiddleware, TokenMiddleware

# https: // blog.51cto.com/u_16099326/11296750
# https: // fund.eastmoney.com/js/fundcode_search.js
# https: // www.jianshu.com/p/d79d3cd62560
# https://blog.csdn.net/zd1007129657/article/details/110429437

# 获取配置文件
config_obj = get_config()
# 创建异步数据库引擎和会话
db_url = get_async_database_url(config_obj)
db_url = f"{db_url}?charset={config_obj.MYSQL_CHARSET}"
engine = create_async_engine(
    db_url,
    pool_size=config_obj.MYSQL_POOL_SIZE,
    max_overflow=config_obj.MYSQL_MAX_OVERFLOW,
    pool_recycle=config_obj.MYSQL_POOL_RECYCLE,
    pool_pre_ping=config_obj.MYSQL_PRE_PING,
    echo=config_obj.MYSQL_ECHO
)
AsyncSession = sessionmaker(
    class_=AsyncSession,
    autocommit=config_obj.MYSQL_AUTO_COMMIT,
    autoflush=config_obj.MYSQL_AUTO_FLUSH,
    expire_on_commit=config_obj.MYSQL_EXPIRE_ON_COMMIT,
    bind=engine)


@asynccontextmanager
# 定义应用生命周期事件
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

# 创建 FastAPI 应用
app = FastAPI(
    title=config_obj.APP_NAME,
    version=config_obj.APP_VERSION,
    description=config_obj.APP_DESCRIPTION,
    lifespan=lifespan,
)

# 最先添加的中间件是最内层，最后添加的中间件是最外层
# 可以理解为是一个栈，最先放入的左后被拿出执行
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(TokenMiddleware, secret_key=config_obj.JWT_SECRET_KEY)
# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router, tags=["/"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
