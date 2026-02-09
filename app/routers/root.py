from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.entity.user import User
from app.queries.user import create_user, get_user_by_username
from app.utils.user import hash_password
from app.utils.server import get_token
from app.routers.base import ResponseDict
from app.utils.const import ReturnCode

root_router = APIRouter()


@root_router.post("/regist")
async def register(params: dict):
    username, password = params.get("username"), params.get("password")
    print(f"{username=}, {password=}")
    user_obj = await get_user_by_username(username)
    print(f"{user_obj=}")
    if user_obj:
        return JSONResponse(
            content=jsonable_encoder(
                ResponseDict(
                    return_code=ReturnCode.USERNAME_EXISTED
                )
            )
        )
    password_salt, password_hash = hash_password(password, None)
    user_obj = User(
        username=username,
        password=password,
        password_salt=password_salt,
        password_hash=password_hash
    )
    user_orm_obj = await create_user(user_obj)

    token = get_token(user_orm_obj.id, user_orm_obj.username)

    return JSONResponse(
        content=jsonable_encoder(ResponseDict(data={"token": token})),
        status_code=status.HTTP_201_CREATED
    )


@root_router.post("/login")
async def login(params: dict):
    username, password = params.get("username"), params.get("password")
    user_obj = await get_user_by_username(username)
    if user_obj is None:
        return JSONResponse(
            content=jsonable_encoder(
                ResponseDict(
                    return_code=ReturnCode.USER_NOT_FOND
                )
            )
        )
    password_salt = user_obj.password_salt
    _, received_password_hash = hash_password(password, password_salt)
    print(f"{received_password_hash=}, {user_obj.password_hash=}")
    if received_password_hash != user_obj.password_hash:
        return JSONResponse(
            content=jsonable_encoder(
                ResponseDict(
                    return_code=ReturnCode.USERNAME_OR_PASSWORD_ERROR
                )
            )
        )
    token = get_token(user_obj.id, user_obj.username)
    return JSONResponse(
        content=jsonable_encoder(ResponseDict(data={"token": token}))
    )
