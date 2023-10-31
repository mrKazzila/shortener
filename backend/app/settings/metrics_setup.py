from prometheus_fastapi_instrumentator import Instrumentator

metrics_instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics"],
)
