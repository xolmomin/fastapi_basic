import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

load_dotenv('.env')


@dataclass
class BaseConfig:
    def asdict(self):
        return asdict(self)


@dataclass
class SmtpConfig(BaseConfig):
    """Mail connection variables"""
    SMTP_USERNAME: str = os.getenv('SMTP_USERNAME')
    SMTP_SERVER: str = os.getenv('SMTP_SERVER')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', 1111))
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')


@dataclass
class DatabaseConfig(BaseConfig):
    """Database connection variables"""
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASS: str = os.getenv('DB_PASS')
    HOST: str = os.getenv('DB_HOST')
    PORT: str = os.getenv('DB_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass
class Configuration:
    """All in one configuration's class"""
    db = DatabaseConfig()
    smtp = SmtpConfig()
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    BROKER_URL: str = os.getenv('BROKER_URL')


conf = Configuration()
