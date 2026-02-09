import secrets
import hashlib
from typing import Optional


def generate_salt():
    # 生成 32 个字节，每个字节会被转换为两个十六进制字符，所以会生成 64 个字符的字符串
    return secrets.token_hex(32)


def hash_password(password: str, password_salt: Optional[str]) -> tuple[str, str]:
    if password_salt is None:
        password_salt = generate_salt()

    # 使用 SHA3-256 算法进行哈希计算，处理的是二进制数据
    # 将密码和盐值转换为字节序列（二进制）
    password_salt_combo = (password + password_salt).encode('utf-8')
    # 哈希后是二进制数据，通过 hexdigest 转换为十六进制字符串进行存储
    password_hash = hashlib.sha3_256(password_salt_combo).hexdigest()
    return password_salt, password_hash
