from datetime import timedelta

from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    postgres_dsn: PostgresDsn = (
        'postgresql+asyncpg://user:pass@127.0.0.1:5432/db')
    redis_dsn: RedisDsn = 'redis://127.0.0.1:6379'
    log_level: str = 'INFO'
    postgres_echo: bool = False

    authjwt_secret_key: str = 'secret'
    authjwt_access_token_expires: timedelta = 600  # 10 минут
    authjwt_refresh_token_expires: timedelta = 604800  # 7 дней
    authjwt_denylist_enabled: bool = True


settings = Settings()
