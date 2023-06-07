import pydantic


class Config(pydantic.BaseSettings):
    log_level: str = "INFO"
    log_file: str = "log.txt"


config = Config()