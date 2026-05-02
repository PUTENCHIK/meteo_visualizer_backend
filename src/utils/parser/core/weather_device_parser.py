import re

from src.schemas import WeatherDeviceName
from src.utils.exceptions import InvalidWeatherDeviceNameError


class WeatherDeviceParser():
    """
    Статичный класс-парсер имён измерительных приборов, приходящих от API
    """

    DEVICE_NAME_REGEX = re.compile(
        r"^(?P<mast>[^-]+)"
        r"-L(?P<yard>\._\d+|\d+)"
        r"(?:-N(?P<num>\d+))?"
        r"-(?P<name>[^-]+)"
        r"(?:-(?P<postfix>.+))?$"
    )

    @staticmethod
    def parse_name(name: str) -> WeatherDeviceName:
        match = WeatherDeviceParser.DEVICE_NAME_REGEX.match(name)
        if not match:
            raise InvalidWeatherDeviceNameError()
        
        data = match.groupdict()

        data['mast'] = data['mast'].lower()
        data['yard'] = int(data['yard'])
        data['num'] = int(data['num']) if data["num"] is not None else 1

        return WeatherDeviceName(**data)
