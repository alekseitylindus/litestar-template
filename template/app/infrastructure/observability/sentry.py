"""Sentry configuration module."""

from collections.abc import Sequence

import sentry_sdk
from sentry_sdk.integrations import Integration


def configure_sentry(
    dsn: str | None,
    environment: str | None,
    integrations: Sequence[Integration] | None = None,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
) -> None:
    """Configure Sentry SDK.

    Args:
        dsn: Sentry DSN string. If None, Sentry will not be initialized.
        environment: Environment name for Sentry.
        integrations: Optional list of Sentry integrations to enable.
        traces_sample_rate: Sample rate for performance monitoring.
        profiles_sample_rate: Sample rate for profiling.
    """
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        integrations=integrations or [],
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
    )
