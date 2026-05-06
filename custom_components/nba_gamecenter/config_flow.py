from __future__ import annotations
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class NBAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NBA GameCenter."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="NBA GameCenter", data={})

        return self.async_show_form(step_id="user", data_schema=None)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return NBAOptionsFlow(config_entry)


class NBAOptionsFlow(config_entries.OptionsFlow):
    """Handle options for NBA GameCenter."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=None)
