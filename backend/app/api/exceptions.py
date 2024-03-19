from fastapi import HTTPException, status

__all__ = (
    "InvalidUrlException",
    "UrlNotFoundException",
)


class InvalidUrlException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid url!",
        )


class UrlNotFoundException(HTTPException):
    def __init__(self, *, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.detail,
        )
