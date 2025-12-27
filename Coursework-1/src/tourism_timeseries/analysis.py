"""Analytical helpers for tourism time-series."""

from __future__ import annotations

from datetime import date
from typing import List, Optional, Tuple

import pandas as pd
from sqlmodel import Session, select

from .models import Observation


def _validate_date(value: date, parameter: str) -> None:
    if not isinstance(value, date):
        raise TypeError(f"{parameter} must be a datetime.date")


def yoy_change(session: Session, series_id: int, month: date) -> Optional[float]:
    """Return the year-on-year percentage change for the given series and month."""

    _validate_date(month, "month")
    current = session.get(Observation, (series_id, month))
    previous_month = month.replace(year=month.year - 1)
    previous = session.get(Observation, (series_id, previous_month))

    if not current or current.value is None:
        return None
    if not previous or previous.value is None:
        return None
    if previous.value == 0:
        return None

    return (current.value - previous.value) / previous.value * 100


def moving_average(
    session: Session,
    series_id: int,
    window: int = 12,
) -> List[Tuple[date, Optional[float]]]:
    """Return a rolling mean time series for the given series."""

    if window <= 0:
        raise ValueError("window must be positive")

    stmt = (
        select(Observation)
        .where(Observation.series_id == series_id)
        .order_by(Observation.month)
    )
    observations = session.exec(stmt).all()
    if not observations:
        return []

    df = pd.DataFrame(
        {"month": [obs.month for obs in observations], "value": [obs.value for obs in observations]}
    )
    df["moving_average"] = df["value"].rolling(window=window, min_periods=window).mean()

    results: List[Tuple[date, Optional[float]]] = []
    for month_value, ma_value in df[["month", "moving_average"]].itertuples(index=False, name=None):
        results.append((month_value, None if pd.isna(ma_value) else float(ma_value)))
    return results


def missing_rate(session: Session, series_id: int, start: date, end: date) -> float:
    """Return proportion of missing values in [start, end] for the series."""

    _validate_date(start, "start")
    _validate_date(end, "end")
    if start > end:
        raise ValueError("start must not be after end")

    stmt = select(Observation).where(
        Observation.series_id == series_id,
        Observation.month >= start,
        Observation.month <= end,
    )
    observations = session.exec(stmt).all()
    if not observations:
        raise ValueError("No observations in the given range")

    missing_count = sum(obs.value is None for obs in observations)
    return missing_count / len(observations)
