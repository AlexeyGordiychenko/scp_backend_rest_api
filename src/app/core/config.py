from typing import Any, Optional
from pydantic import Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = Field("0.0.1", env="VERSION")
    PROJECT_NAME: str = Field("ShopAPI", env="PROJECT_NAME")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_ECHO: bool = Field(False, env="POSTGRES_ECHO")
    POSTGRES_POOL_SIZE: int = Field(5, env="POSTGRES_POOL_SIZE")
    POSTGRES_URI: Optional[PostgresDsn] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

    @field_validator("POSTGRES_URI", mode="before")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=int(info.data.get("POSTGRES_PORT")),
            path=info.data.get("POSTGRES_DB"),
        )


settings = Settings()
