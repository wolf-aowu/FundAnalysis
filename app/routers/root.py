from fastapi import APIRouter

root_router = APIRouter()


@root_router.post("/login")
async def login(params: dict):
    print(f"Login params: {params}")
    return {"message": "Login endpoint"}
