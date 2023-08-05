import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database.base.base_model import BaseModel


class BaseImage(BaseModel):
    __abstract__ = True
    file_unique_id = sa.Column(sa.String(255), nullable=False, unique=True)
    photo_id = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)


class DeviceImages(BaseImage):
    __tablename__ = 'devices_images'
    device_id = sa.Column(
        sa.Integer, sa.ForeignKey('devices.id', ondelete="CASCADE"))
    device = relationship('Device', back_populates='image')


class DoneJobImages(BaseImage):
    __tablename__ = 'done_job_images'
    pass
