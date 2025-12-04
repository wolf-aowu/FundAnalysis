from functools import wraps


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        from main import AsyncSession
        async with AsyncSession() as session:
            return await func(session, *args, **kwargs)
    return wrapper
