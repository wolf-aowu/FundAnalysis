import jwt
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.routers.base import ResponseDict
from app.utils.const import ReturnCode
from app.utils.config import get_config

token_exclude_router_paths = ["/", "/login", "/regist"]


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        print("=====ProcessTime=====")
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        print(f"后端响应时间: {process_time}s")
        return response


# TODO 自动解析 token 中的数据的功能还没有测试
class TokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key):
        super().__init__(app)
        self.secret_key = secret_key

    async def dispatch(self, request, call_next):
        print("=====Token=====")
        request_path = request.url.path
        # print(f"{request_path=}")
        # 不是排除的路由路径 进行 token 检查
        if request_path not in token_exclude_router_paths:
            header = request.headers.get('Authorization')
            if not header:
                return JSONResponse(ResponseDict(return_code=ReturnCode.TOKEN_NOT_EXISTED))
            try:
                config_obj = get_config()
                payload = jwt.decode(header, self.secret_key, algorithms=["HS256"])
                print(f"{payload=}")
                # print(request.state.user)
            except jwt.ExpiredSignatureError:
                return JSONResponse(ResponseDict(return_code=ReturnCode.TOKEN_EXPIRE))
            except jwt.InvalidTokenError:
                return JSONResponse(ResponseDict(return_code=ReturnCode.TOKEN_ERROR))
            except Exception as e:
                return JSONResponse(ResponseDict(return_code=ReturnCode.FAILURE))

        response = await call_next(request)
        return response
