from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pyquery==1.3.0']

from pyquery import PyQuery as pq
import urllib


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([TemperatureSensor(), HumiditySensor(),BatterySensor()])


def parse_weather_logger(parseSelect, attrName):
    try:
        dom = pq(url='http://192.168.178.54/livedata.htm', parser='html')
        nodes = dom('select' if parseSelect else 'input')
        if parseSelect:
            tagWithValue = nodes('[name="{0}"] option:selected'.format(attrName))
        else:
            tagWithValue = nodes('[name="{0}"]'.format(attrName))
        return tagWithValue.attr('value')
    except:
        return None

class TemperatureSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    def update(self):
        self._state = parse_weather_logger(False,'inTemp')

class HumiditySensor(Entity):

    def __init__(self):
        self._state = None

    @property
    def name(self):
        return 'huminity'

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return '%'

    def update(self):
        self._state = parse_weather_logger(False,'inHumi')

class BatterySensor(Entity):

    def __init__(self):
        self._state = None

    @property
    def name(self):
        return 'battery_level'

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return '🔋'

    def update(self):
        self._state = 'Normal' if parse_weather_logger(True,'inBattSta') == '0' else 'Low'
