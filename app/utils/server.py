import jwt
from datetime import datetime, timedelta, timezone
from app.utils.config import get_config


def get_token(user_id, username):
    config_obj = get_config()
    expire_minutes = config_obj.JWT_EXPIRE_MINUTES
    secret_key = config_obj.JWT_SECRET_KEY
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {
        "user_id": user_id,
        "user_name": username,
        "exp": expire_time
    }

    token = jwt.encode(
        payload=payload,
        key=secret_key,
        algorithm="HS256"
    )

    print(f"{token=}")

    return token
