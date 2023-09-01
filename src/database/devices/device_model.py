import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database.base.base_model import BaseModel
from src.database.images.image_model import DeviceImages


class Device(BaseModel):
    __tablename__ = 'devices'
    name = sa.Column(sa.String(199), nullable=False)
    price = sa.Column(sa.Text, nullable=False)
    is_avaible = sa.Column(sa.Boolean, nullable=True)
    image = relationship('DeviceImages', back_populates='device',
                         cascade="all, delete",
                         passive_deletes=True, uselist=False)
    description = sa.Column(sa.Text)
