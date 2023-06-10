import pydantic


class Config(pydantic.BaseSettings):
    app_name: str = "default"
    log_level: str = "INFO"
    log_file: str = "log.txt"
    message_broker_host: str = "localhost"
    message_broker_queue: str = "main"


config = Config()
