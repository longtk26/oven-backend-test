from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    db_name: str = Field(env="DB_NAME")
    db_user: str = Field(env="DB_USER")
    db_password: str = Field(env="DB_PASSWORD")
    db_host: str = Field(env="DB_HOST")
    db_port: int = Field(env="DB_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()