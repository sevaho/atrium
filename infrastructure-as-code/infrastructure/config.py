from pydantic_settings import BaseSettings
from pydantic.types import SecretStr

from pydantic.networks import IPv4Address

try:  # nosec
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:  # nosec
    pass


class Config(BaseSettings):
    DIGITALOCEAN_TOKEN: SecretStr
    SPACES_ACCESS_KEY_ID: SecretStr
    SPACES_SECRET_ACCESS_KEY: SecretStr
    ASIC_SERVER_HETZNER_HOST: IPv4Address


config = Config()

__all__ = ["config"]
