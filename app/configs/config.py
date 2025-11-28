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


class TestingConfig(Config):
    ENV = "Testing"
    pass


class ProductionConfig(Config):
    ENV = "Production"
    pass
