# 放数据库相关方法
from app.utils.config import get_config
from dataclasses import fields


def get_database_url(config_obj) -> str:
    config_obj = config_obj or get_config()
    db_host = config_obj.MYSQL_HOST
    db_port = config_obj.MYSQL_PORT
    db_username = config_obj.MYSQL_USER
    db_password = config_obj.MYSQL_PASSWORD
    db_name = config_obj.APP_NAME
    db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db_url


def get_async_database_url(config_obj) -> str:
    config_obj = config_obj or get_config()
    db_host = config_obj.MYSQL_HOST
    db_port = config_obj.MYSQL_PORT
    db_username = config_obj.MYSQL_USER
    db_password = config_obj.MYSQL_PASSWORD
    db_name = config_obj.APP_NAME
    db_url = f"mysql+aiomysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db_url


def to_orm(orm_class, entity_obj):
    orm_obj = orm_class()
    for field in fields(entity_obj):
        if field.name.startswith("__"):
            continue
        if hasattr(orm_obj, field.name):
            value = getattr(entity_obj, field.name)
            setattr(orm_obj, field.name, value)
    return orm_obj


def to_entity(entity_class, orm_obj):
    if orm_obj is None:
        return None
    entity_obj = entity_class()
    for field_name in entity_class.__dataclass_fields__.keys():
        if field_name.startswith("__"):
            continue
        if hasattr(orm_obj, field_name):
            value = getattr(orm_obj, field_name)
            setattr(entity_obj, field_name, value)
    return entity_obj
