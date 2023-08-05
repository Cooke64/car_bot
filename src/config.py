import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN")
    __ADMINS_ID: str = os.environ.get("ADMINS_ID")
    USERNAME: str = os.environ.get("USERNAME")
    PASSWORD: str = os.environ.get("PASSWORD")
    HOST: str = os.environ.get("HOST")
    PORT: str = os.environ.get("PORT")
    DATABASE: str = os.environ.get("DATABASE")
    DEBUG: bool = True

    @property
    def admins_id_list(self):
        return [int(x) for x in self.__ADMINS_ID.split(',')]

    @property
    def DATABASE_URL(self):
        if self.DEBUG:
            return 'postgresql://postgres:12345678@localhost:5432/akm'
        return f'postgresql://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'


settings = Settings()
