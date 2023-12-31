from sqlalchemy import Column as _, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = _(
        Integer(), nullable=False,
        unique=True, primary_key=True, autoincrement=True
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)