from dataclasses import dataclass

from fastapi import APIRouter, status

router = APIRouter(
    prefix='/api/healthcheck',
    tags=['healthcheck'],
)


@dataclass(frozen=True)
class HealthcheckStatus:
    status: str = 'ok'


OK_STATUS = HealthcheckStatus()


@router.get(
    path='/',
    name='Simple healthchecker',
    status_code=status.HTTP_200_OK,
)
async def get_status() -> HealthcheckStatus:
    """
    Returns the health status of the application.

    Returns:
        HealthcheckStatus: A dataclass representing the health status,
        with a default status of 'ok'.
    """
    return OK_STATUS
