import sqlalchemy as sa

from src.bot.database.base.base_model import BaseModel


class Device(BaseModel):
    __tablename__ = 'devices'
    name = sa.Column(sa.String(199), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    price = sa.Column(sa.Text, nullable=False)
    is_avaible = sa.Column(sa.Boolean, nullable=False)
