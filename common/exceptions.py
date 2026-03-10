from fastapi import HTTPException


class HTTPExceptions:
    @staticmethod
    def http_400(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=400, detail=detail)

    @staticmethod
    def http_401(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=401, detail=detail)

    @staticmethod
    def http_403(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=403, detail=detail)

    @staticmethod
    def http_404(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=404, detail=detail)

    @staticmethod
    def http_409(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=409, detail=detail)

    @staticmethod
    def http_422(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=422, detail=detail)

    @staticmethod
    def http_500(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=500, detail=detail)

    @staticmethod
    def http_502(msg: str, e: Exception = None) -> HTTPException:
        detail = f"{msg}" if e is None else f"{msg}: {e}"
        return HTTPException(status_code=502, detail=detail)
