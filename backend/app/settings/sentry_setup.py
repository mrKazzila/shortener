import logging
from sys import exit

import sentry_sdk

from app.settings.config import settings

logger = logging.getLogger(__name__)


def sentry_setup() -> None:
    """Sentry setup."""
    try:
        if settings().MODE != 'TEST':
            logger.info('Start sentry setup')
            sentry_sdk.init(
                dsn=settings().sentry.SENTRY_URL,
                traces_sample_rate=settings().sentry.TRACES_SAMPLE_RATE,
                profiles_sample_rate=settings().sentry.PROFILES_SAMPLE_RATE,
            )
            logger.info('Sentry setup successfully ended')
        else:
            logger.info(
                'Skit sentry setup for this mode type. %(mode)s',
                {'mode': settings().MODE},
            )

    except Exception as e:
        logger.error('Sentry setup with error: %(error)s', {'error': e})
        exit(e)
