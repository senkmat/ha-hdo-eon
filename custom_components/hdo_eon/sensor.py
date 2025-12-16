from homeassistant.components.sensor import SensorEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Tato funkce řekne HA, aby přidal náš senzor."""
    async_add_entities([EonHdoCodeSensor()])

class EonHdoCodeSensor(SensorEntity):
    """Senzor, který zatím jen ukazuje váš kód."""
    _attr_name = "E.ON HDO Konfigurace"
    _attr_unique_id = "eon_hdo_config_code"
    
    @property
    def native_value(self):
        return "A1B6DP5" # Váš kód, který budeme později používat pro výpočty
