import os
import typing


class Config:
    _config: typing.Any = None
    port: str = ""
    discord_webhook: str = ""
    mongo_url: str = "mongodb://user:passw@localhost:27017/api"
    mongo_data_collection: str = "data"
    mongo_data_database: str = "api"
    mongo_auth_collection: str = "auths"
    mongo_auth_database: str = "api"
    flask_env: str = ""
    _options: typing.List[str] = [
        "port",
        "discord_webhook",
        "mongo_url",
        "mongo_data_collection",
        "mongo_data_database",
        "mongo_auth_collection",
        "mongo_auth_database",
        "flask_env"
    ]

    def __new__(cls) -> typing.Any:  # needs to be typed as a class instance
        if cls._config is not None:
            return cls._config
        cls._config = super().__new__(cls)
        cls._config._load_from_environment_variables()
        return cls._config

    def _load_from_environment_variables(self) -> None:
        for option in self._options:
            self.__setattr__(option, os.getenv(option.upper(), self.__getattribute__(option)))


CONFIG = Config()
