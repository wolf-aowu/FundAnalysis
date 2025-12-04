from fastapi import APIRouter
from app.queries.user import get_user_by_username

root_router = APIRouter()


@root_router.post("/login")
async def login(params: dict):
    print(f"Login params: {params}")
    username, password = params.get("username"), params.get("password")
    user_obj = await get_user_by_username(username)
    print(f"Retrieved user: {user_obj}")
    return {"message": "Login endpoint"}
