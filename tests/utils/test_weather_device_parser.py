import pytest

from src.schemas import WeatherDeviceName
from src.utils.exceptions import InvalidWeatherDeviceNameError
from src.utils.parser import WeatherDeviceParser


class TestWeatherDeviceParser:
    def test_parse_name__valid_name__no_exceptions(self):
        """
        Проверка на возвращение ожидаемого объекта WeatherDeviceName при передаче
        валидного названия датчика
        """

        # Подготовка
        mast_name = "South"
        yard_number = 1
        station_number = 1
        device_name = "WeatherDevice"
        name = f"{mast_name}-L{yard_number}-N{station_number}-{device_name}"

        # Действие
        result = WeatherDeviceParser.parse_name(name)

        # Проверка
        assert isinstance(result, WeatherDeviceName)
        assert result.mast == mast_name.lower()
        assert result.yard == yard_number
        assert result.num == station_number
        assert result.name == device_name
        assert result.postfix is None

    def test_parse_name__valid_name_without_num__no_exceptions(self):
        """
        Проверка на возвращение ожидаемого объекта WeatherDeviceName при передаче
        валидного названия датчика без указанного номера станции
        """

        # Подготовка
        mast_name = "North"
        yard_number = 2
        device_name = "WindDetector"
        name = f"{mast_name}-L{yard_number}-{device_name}"

        # Действие
        result = WeatherDeviceParser.parse_name(name)

        # Проверка
        assert isinstance(result, WeatherDeviceName)
        assert result.mast == mast_name.lower()
        assert result.yard == yard_number
        assert result.num == 1
        assert result.name == device_name
        assert result.postfix is None

    def test_parse_name__name_without_mast_name__invalid_name_exception(self):
        """
        Проверка на исключение InvalidWeatherDeviceNameError при передаче имени без
        указания мачты
        """

        # Подготовка
        mast_name = ""
        yard_number = 2
        device_name = "WindDetector"
        name = f"{mast_name}-L{yard_number}-{device_name}"

        # Действие и проверка
        with pytest.raises(InvalidWeatherDeviceNameError):
            WeatherDeviceParser.parse_name(name)
