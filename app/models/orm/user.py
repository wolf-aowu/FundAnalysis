from sqlalchemy import Column, String, DateTime
from datetime import datetime

from app.models.orm.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    username = Column(String(50), unique=True)
    # 自用
    password = Column(String(128), comment="明文密码")
    # 密码使用哈希存储可以避免数据库泄露时明文密码被获取的风险
    # 密码加盐处理，可以防止彩虹表攻击，提高密码存储的安全性
    # 每个密码添加随机值作为盐值，即使两个用户使用相同的密码，存储的哈希值也会不同
    password_salt = Column(String(64), comment="密码盐值")
    password_hash = Column(String(256), comment="密码哈希值")
    mobile_phone = Column(String(16), comment="手机号")
    last_login_time = Column(DateTime, default=datetime.now(), comment="上次登录时间")
