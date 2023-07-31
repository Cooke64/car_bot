import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN")
    DATABASE_URL: str = 'postgresql://postgres:12345678@localhost:5432/akm'
    __ADMINS_ID: str = os.environ.get("ADMINS_ID")

    @property
    def admins_id_list(self):
        return [int(x) for x in self.__ADMINS_ID.split(',')]


settings = Settings()
