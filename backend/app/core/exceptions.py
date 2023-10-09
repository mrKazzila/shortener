from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self, *, detail: str | None) -> None:
        self.detail = detail or 'Some problem'
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail,
        )


class UrlNotFoundException(HTTPException):
    def __init__(self, *, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.detail,
        )
