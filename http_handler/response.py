from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder


class ResponseHandler():
    def __init__(self):
        self.response = {}
        self.status_code: int = 200
        self.headers = dict()
        self.cookies = []
        self.buffer = None
        
    def generate_response(self):
        res = JSONResponse(content=jsonable_encoder(obj=self.response), status_code=self.status_code, headers=jsonable_encoder(self.headers))
        for cookie in self.cookies:
            res.set_cookie(**cookie)

        return res

    def generate_stream_response(self):
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        res = StreamingResponse(content=self.buffer, status_code=self.status_code, headers=jsonable_encoder(self.headers), media_type=media_type)
        return res

    def set_header(self,new_header):
        self.headers.update(new_header)

    def set_response(self, data):
        self.response.update(data)

    def set_status_code(self, status_code):
        self.status_code = status_code

    def set_cookie(self, key: str, value: str, path: str="/", max_age: int | None = None, httponly: bool = True, secure: bool = True, samesite: str = "lax"):
        self.cookies.append({
            "key": key,
            "value": value,
            "path": path,
            "max_age": max_age,
            "httponly": httponly,
            "secure": secure,
            "samesite": samesite,
        })

    def set_buffer_data(self, buffer):
        self.buffer = buffer
