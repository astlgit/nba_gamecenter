from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class NBAGameCenterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NBA GameCenter."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:

        # No user options needed — just create the entry
        if user_input is not None:
            return self.async_create_entry(
                title="NBA GameCenter",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )


class NBAGameCenterOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for NBA GameCenter."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:

        # No options yet — but this enables the Config tab
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        defaults: dict[str, Any] = {
            **self.config_entry.data,
            **self.config_entry.options,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )


async def async_get_options_flow(
    config_entry: config_entries.ConfigEntry,
) -> NBAGameCenterOptionsFlowHandler:
    return NBAGameCenterOptionsFlowHandler(config_entry)
