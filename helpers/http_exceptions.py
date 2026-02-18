from fastapi import HTTPException


class HTTP_Exceptions:
    @staticmethod
    def http_400(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=400, detail=f"{msg}: {e}")

    @staticmethod
    def http_401(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=401, detail=f"{msg}: {e}")

    @staticmethod
    def http_403(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=403, detail=f"{msg}: {e}")

    @staticmethod
    def http_404(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=404, detail=f"{msg}")

    @staticmethod
    def http_409(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=409, detail=f"{msg}: {e}")

    @staticmethod
    def http_422(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=422, detail=f"{msg}: {e}")

    @staticmethod
    def http_500(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=500, detail=f"{msg}: {e}")

    @staticmethod
    def http_502(msg: str, e: Exception = None) -> HTTPException:
        return HTTPException(status_code=502, detail=f"{msg}: {e}")