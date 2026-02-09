from functools import wraps


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        from main import AsyncSession
        async with AsyncSession() as session:
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    return wrapper
