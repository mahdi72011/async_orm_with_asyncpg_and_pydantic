from pydantic_settings import BaseSettings, SettingsConfigDict




class DBSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    postgres_password: str
    db_database: str
    db_min_connection_pool: int
    db_max_connection_pool: int

    model_config = SettingsConfigDict(
        env_file=".env.example",
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        extra="ignore"
    )


db_settings = DBSettings()