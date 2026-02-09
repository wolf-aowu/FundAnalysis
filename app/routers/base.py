from app.utils.const import ReturnCode


class ResponseDict(dict):
    def __init__(self, return_code: ReturnCode = ReturnCode.SUCCESS, data: dict = None, **kwargs):
        super().__init__()
        code, message, comments = return_code.value
        success = not bool(code)
        self.update(code=code, message=message, success=success)
        if data is not None:
            self.update(data=data)
        if kwargs:
            self.update(kwargs)
