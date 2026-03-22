"""Naver Search API client for blog, news, and cafe article collection.

Supports paginated retrieval with date-range filtering across three channels
(blog, news, cafearticle) used in the infovail-iq data ingestion pipeline.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from typing import Literal

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

Channel = Literal["blog", "news", "cafearticle"]

_ENDPOINTS: dict[str, str] = {
    "blog": "https://openapi.naver.com/v1/search/blog",
    "news": "https://openapi.naver.com/v1/search/news",
    "cafearticle": "https://openapi.naver.com/v1/search/cafearticle",
}

_MAX_DISPLAY = 100  # max items per single API call
_MAX_START = 1000  # API pagination ceiling


class NaverClient:
    """Thin wrapper around the Naver Search API.

    Usage::

        with NaverClient() as client:
            results = client.collect(
                keyword="코로나 백신 이물질",
                channel="news",
                date_from="2026-02-07",
                date_to="2026-03-21",
            )
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        self.client_id = client_id or os.getenv("NAVER_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("NAVER_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "NAVER_CLIENT_ID and NAVER_CLIENT_SECRET must be provided "
                "via arguments or .env file."
            )
        self._http = httpx.Client(
            headers={
                "X-Naver-Client-Id": self.client_id,
                "X-Naver-Client-Secret": self.client_secret,
            },
            timeout=30.0,
        )

    # ------------------------------------------------------------------
    # Low-level: single API call
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        channel: Channel = "blog",
        display: int = 100,
        start: int = 1,
        sort: Literal["sim", "date"] = "date",
    ) -> dict:
        """Execute a single search request and return the raw JSON response."""
        url = _ENDPOINTS[channel]
        params = {
            "query": query,
            "display": min(display, _MAX_DISPLAY),
            "start": min(start, _MAX_START),
            "sort": sort,
        }
        resp = self._http.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # High-level: paginated collection with date filtering
    # ------------------------------------------------------------------

    def collect(
        self,
        keyword: str,
        channel: Channel = "blog",
        date_from: str | None = None,
        date_to: str | None = None,
        max_results: int = 1000,
        sort: Literal["sim", "date"] = "date",
    ) -> list[dict]:
        """Paginate through search results, optionally filtering by date.

        Args:
            keyword: Search query string.
            channel: ``"blog"``, ``"news"``, or ``"cafearticle"``.
            date_from: Inclusive start date, ``"YYYY-MM-DD"``.
            date_to: Inclusive end date, ``"YYYY-MM-DD"``.
            max_results: Cap on total items to return (API hard-cap ≈ 1 100).
            sort: ``"date"`` (newest first) or ``"sim"`` (relevance).

        Returns:
            A list of normalised result dicts.
        """
        results: list[dict] = []
        start = 1
        # Naver caps at start=1000 + display=100 → 1099 reachable items
        api_cap = min(max_results, _MAX_START + _MAX_DISPLAY - 1)

        dt_from = _parse_date_str(date_from) if date_from else None
        dt_to = _parse_date_str(date_to) if date_to else None

        while start <= api_cap and len(results) < max_results:
            display = min(_MAX_DISPLAY, max_results - len(results))

            try:
                data = self.search(
                    query=keyword,
                    channel=channel,
                    display=display,
                    start=start,
                    sort=sort,
                )
            except httpx.HTTPStatusError as exc:
                logger.error("API error (start=%d): %s", start, exc)
                break

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                row = _normalize(item, channel, keyword)
                if _in_date_range(row, dt_from, dt_to):
                    results.append(row)

            # Early termination: when sorted by date, once the last item in
            # the page falls before date_from there is no point fetching more.
            if sort == "date" and dt_from and items:
                last_pub = _normalize(items[-1], channel, keyword).get("pub_date")
                if last_pub and _strip_tz(last_pub) < dt_from:
                    break

            start += display
            time.sleep(0.1)  # courtesy delay

        logger.info(
            "Collected %d items | keyword=%r channel=%s",
            len(results),
            keyword,
            channel,
        )
        return results

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> NaverClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# ======================================================================
# Module-private helpers
# ======================================================================

_DATE_FORMATS = ("%Y%m%d", "%a, %d %b %Y %H:%M:%S %z")


def _parse_date_str(s: str) -> datetime:
    """Parse a ``YYYY-MM-DD`` user-supplied date string."""
    return datetime.strptime(s, "%Y-%m-%d")


def _parse_api_date(raw: str) -> datetime | None:
    """Parse the date string returned by the Naver API.

    Blog/cafe use ``"20260304"``; news uses RFC-822 ``"Tue, 04 Mar 2026 …"``.
    """
    if not raw:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw.strip(), fmt)
        except ValueError:
            continue
    return None


def _normalize(item: dict, channel: Channel, keyword: str) -> dict:
    """Map a raw API item to a flat, channel-agnostic dict."""
    pub_date = _parse_api_date(
        item.get("postdate") or item.get("pubDate", "")
    )
    return {
        "title": item.get("title", ""),
        "description": item.get("description", ""),
        "link": item.get("link", ""),
        "original_link": item.get("originallink", item.get("link", "")),
        "pub_date": pub_date,
        "channel": channel,
        "keyword": keyword,
        "blogger_name": item.get("bloggername", ""),
        "cafe_name": item.get("cafename", ""),
        "cafe_url": item.get("cafeurl", ""),
    }


def _strip_tz(dt: datetime) -> datetime:
    """Drop timezone info so naive/aware datetimes can be compared."""
    return dt.replace(tzinfo=None)


def _in_date_range(
    item: dict,
    dt_from: datetime | None,
    dt_to: datetime | None,
) -> bool:
    """Return *True* if the item's pub_date falls within [dt_from, dt_to]."""
    pub = item.get("pub_date")
    if pub is None:
        return True  # keep items without a parseable date
    d = _strip_tz(pub)
    if dt_from and d < dt_from:
        return False
    if dt_to and d > dt_to.replace(hour=23, minute=59, second=59):
        return False
    return True
