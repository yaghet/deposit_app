from fastapi import HTTPException


class WalletNotFoundException(HTTPException):
    def __init__(self, detail: str = "Wallet Not Found") -> None:
        super().__init__(status_code=404, detail=detail)


class InvalidOperationException(HTTPException):
    def __init__(self, detail: str = "Invalid Operation Type") -> None:
        super().__init__(status_code=400, detail=detail)


class OperationExecutionException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=400, detail=detail)
