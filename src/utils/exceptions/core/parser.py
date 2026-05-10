class InvalidWeatherDeviceNameError(ValueError):
    def __init__(self):
        super().__init__(
            "Формат переданной строки не соответствует заданному формату наименования "
            "измерительных приборов API"
        )
