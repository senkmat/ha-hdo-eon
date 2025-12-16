import logging
import aiohttp
import async_timeout
from datetime import datetime
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

# Upravená URL na vyhledávací endpoint
HDO_URL = "https://www.egd.cz/hdo-casy-platnosti-nizkeho-tarifu"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([EonHdoSensor()], True)

class EonHdoSensor(SensorEntity):
    _attr_name = "E.ON HDO Status"
    _attr_unique_id = "eon_hdo_status_api"

    def __init__(self):
        self._state = "Inicializace"
        self._hdo_code = "A1B6DP5"

    @property
    def native_value(self):
        return self._state

    async def async_update(self):
        """Stažení dat s identifikací prohlížeče."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        params = {"code": self._hdo_code}

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(HDO_URL, headers=headers, params=params) as response:
                        if response.status == 200:
                            html_text = await response.text()
                            # Tady budeme hledat klíčové slovo v HTML
                            if "Nízký tarif" in html_text:
                                self._state = "Data přijata"
                            else:
                                self._state = "Kód nenalezen"
                        else:
                            self._state = f"Chyba {response.status}"
        except Exception as e:
            _LOGGER.error("Chyba HDO: %s", e)
            self._state = "Chyba sítě"
