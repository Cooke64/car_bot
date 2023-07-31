import sqlalchemy as sa

from src.bot.database.base.base_model import BaseModel


class BaseImage(BaseModel):
    __abstract__ = True
    file_unique_id = sa.Column(sa.String(255), nullable=False, unique=True)
    photo_id = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)


class DeviceImages(BaseImage):
    __tablename__ = 'device_images'
    pass


class DoneJobImages(BaseImage):
    __tablename__ = 'done_job_images'
    pass
