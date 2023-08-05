import sqlalchemy as sa
from pydantic import BaseModel as PyModel
from sqlalchemy.orm import relationship

from src.database.base.base_model import BaseModel


class CarBrend(BaseModel):
    __tablename__ = 'cars_brends'
    name = sa.Column(sa.String(199), nullable=False)
    models = relationship('Model', back_populates='car_brend')
    car_coef = sa.Column(sa.Float, nullable=False)


class Model(BaseModel):
    __tablename__ = 'models'
    name = sa.Column(sa.String(199), nullable=False)
    car_brend_id = sa.Column(sa.Integer, sa.ForeignKey('cars_brends.id'))
    car_brend = relationship('CarBrend', back_populates='models')
    coef = sa.Column(sa.Float, nullable=False)


class BrendModelShema(PyModel):
    brend_name: str | None
    brend_coef: float | None
    model_name: str | None
    model_coef: float | None
