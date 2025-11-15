from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# https: // blog.51cto.com/u_16099326/11296750
# https: // fund.eastmoney.com/js/fundcode_search.js
# https: // www.jianshu.com/p/d79d3cd62560
# https://blog.csdn.net/zd1007129657/article/details/110429437

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
