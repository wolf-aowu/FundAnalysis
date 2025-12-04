from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User():
    id: Optional[int]
    username: str
    password_salt: Optional[str]
    password_hash: Optional[str]
    mobile_phone: Optional[str]
    last_login_time: Optional[str]
    _create_time: Optional[datetime]
