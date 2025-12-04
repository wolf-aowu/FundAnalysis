
from sqlalchemy import select
from app.queries.base import with_session
from app.models.orm.user import User as UserORM
from app.models.entity.user import User
from app.utils.database import to_entity


@with_session
async def get_user_by_username(session, username: str) -> User:
    result = await session.execute(select(UserORM).where(UserORM.username == username))
    user_orm_obj = result.scalars().first()
    user_obj = to_entity(User, user_orm_obj)
    return user_obj


@with_session
async def get_password_salt_and_hash(session, user_id: int):
    result = await session.execute(select(UserORM).where(UserORM.id == user_id))
    user_orm_obj = result.scalars().first()
    user_obj = to_entity(User, user_orm_obj)
    return user_obj.password_salt, user_obj.password_hash
