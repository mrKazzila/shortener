from dataclasses import dataclass

__all__ = ("OK_STATUS",)


@dataclass(frozen=True)
class HealthcheckStatus:
    status: str = "ok"


OK_STATUS = HealthcheckStatus()
