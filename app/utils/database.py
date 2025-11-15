# 放数据库相关方法
from app.utils.config import get_config


def get_database_url(config_obj) -> str:
    config_obj = config_obj or get_config()
    db_host = config_obj.MYSQL_HOST
    db_port = config_obj.MYSQL_PORT
    db_username = config_obj.MYSQL_USER
    db_password = config_obj.MYSQL_PASSWORD
    db_name = config_obj.APP_NAME
    db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db_url
