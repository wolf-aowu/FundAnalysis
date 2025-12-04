__all__ = [
    "Config",
    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig"
]


class Config:
    ENV = "Base"
    ENV_KEY = "fund_analysis_env"
    APP_NAME = "fund_analysis"
    APP_VERSION = "0.1.0"
    APP_DESCRIPTION = "一个分析和管理个人基金的应用，主要功能：1. 计算基金每日涨跌幅 2. 管理买入卖出份数"
    APP_HOST = "127.0.0.1"
    APP_PORT = "8000"
    MYSQL_CHARSET = "utf8mb4"


class DevelopmentConfig(Config):
    ENV = "Development"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_CHARSET = "utf8mb4"
    # 实际最大连接数 = MYSQL_POOL_SIZE + MYSQL_MAX_OVERFLOW，MySQL 默认最大连接数是 151，最大连接数是 100000
    MYSQL_POOL_SIZE = 20  # 连接池大小，不会立即创建，控制连接复用率避免频繁创建连接
    MYSQL_MAX_OVERFLOW = 131  # 允许在高并发时临时增加的连接数，立即创建
    MYSQL_POOL_RECYCLE = 3600  # 连接最大回收时间（秒），避免数据库主动断开连接导致连接失效，MySQL 会自动断开空闲超过 8 小时的连接
    MYSQL_PRE_PING = True  # 连接健康检查
    MYSQL_AUTO_COMMIT = False  # 每次操作不立即提交事务，需要手动 commit
    MYSQL_AUTO_FLUSH = False  # 查询前不自动将未提交的更改同步到数据库
    MYSQL_EXPIRE_ON_COMMIT = True  # 提交事务后使所有对象过期，下次访问时重新加载，默认 True
    MYSQL_ECHO = True  # 控制台打印 SQL 日志


class TestingConfig(Config):
    ENV = "Testing"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_POOL_SIZE = 20
    MYSQL_MAX_OVERFLOW = 131
    MYSQL_POOL_RECYCLE = 3600
    MYSQL_PRE_PING = True
    MYSQL_ECHO = True


class ProductionConfig(Config):
    ENV = "Production"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_POOL_SIZE = 20
    MYSQL_MAX_OVERFLOW = 7480
    MYSQL_POOL_RECYCLE = 3600
    MYSQL_PRE_PING = True
    MYSQL_ECHO = False
