from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..api.client import NBAApiClient
from ..api.playoff_api import NBAPLAYOFFAPI
from ..api.live_api import NBALiveAPI

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=30)


class NBAGameCenterCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Central coordinator for NBA GameCenter."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._session = aiohttp.ClientSession()
        self._client = NBAApiClient(self._session)
        self._playoff_api = NBAPLAYOFFAPI(self._client)
        self._live_api = NBALiveAPI(self._client)

        super().__init__(
            hass,
            _LOGGER,
            name="NBA GameCenter Coordinator",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        series_data = await self._playoff_api.get_series_data()
        live_data = await self._live_api.get_live_series_data()

        return {
            "series": series_data,
            "live": live_data,
        }

    async def async_close(self) -> None:
        await self._session.close()
