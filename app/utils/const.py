from enum import Enum


class ReturnCode(Enum):
    # TODO 需要写一个重新编号的工具，这样可以节省编号数量
    SUCCESS = (0, "成功", "一切正常")
    FAILURE = (1, "失败", "后端报错了")
    TOKEN_NOT_EXISTED = (10000, "token 不存在", "token 不存在")
    TOKEN_ERROR = (10001, "token 错误", "token 不对，可能有人在攻击网站或窃取信息")
    TOKEN_EXPIRE = (10002, "token 过期", "token 过期")
    USERNAME_EXISTED = (10003, "用户名已存在", "用户名已存在")
    USER_NOT_FOND = (10004, "用户名或密码错误", "用户不存在")
    USERNAME_OR_PASSWORD_ERROR = (10005, "用户名或密码错误", "用户名或密码错误")

    def __init__(self, code: int, message: str, comments: str):
        self.code = code
        self.message = message
        self.comments = comments
