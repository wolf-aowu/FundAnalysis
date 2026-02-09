from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User():
    id: Optional[int] = None
    username: Optional[int] = None
    password: Optional[int] = None
    password_salt: Optional[int] = None
    password_hash: Optional[int] = None
    mobile_phone: Optional[int] = None
    last_login_time: Optional[int] = None
    _create_time: Optional[int] = None
