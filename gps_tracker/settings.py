import os


class Config:
    def __init__(self) -> None:
        self.port: str = os.getenv("PORT", "5000")
        self.flask_env: str = os.getenv("FLASK_ENV", "DEBUG")
        self.discord_webhook: str = os.getenv("DISCORD_WEBHOOK", "https://discordapp.com/api/webhooks/")

        # mongo
        self.mongo_url: str = os.getenv("MONGO_URL", "mongodb://user:passw@localhost:27017/api")
        self.mongo_auth_database: str = os.getenv("MONGO_AUTH_DATABASE", "api")
        self.mongo_auth_collection: str = os.getenv("MONGO_AUTH_COLLECTION", "auths")
        self.mongo_data_database: str = os.getenv("MONGO_DATA_DATABASE", "api")
        self.mongo_data_collection: str = os.getenv("MONGO_DATA_COLLECTION", "data")


CONFIG = Config()
