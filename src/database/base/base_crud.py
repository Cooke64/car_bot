from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Query, Session, sessionmaker

from src.config import settings
from src.database.base.base_model import BaseModel


class BaseCrud:
    def __init__(self):
        self.session: Session = self.__create_session()

    @staticmethod
    def __create_session():
        engine = create_engine(settings.DATABASE_URL, future=True)
        session_local = sessionmaker(bind=engine)
        return session_local()

    def get_all_items(self, Model: Any) -> list[Any] | None:
        return self.session.query(Model).all()

    def get_current_item(self, id_item: int, Model: Any) -> Query:
        """Возвращает Объект построения SQL на уровне ORM.
        :param id_item: первичный ключ
        :type id_item: int
        :param Model: класс модели базы данных
        :type Model: Any
        :rtype: Query
        :return: ORM-level SQL construction object. | raise NotFound
        """
        query = self.session.query(Model).filter(Model.id == id_item)
        return query

    def create_item(self, item: Any) -> Any:
        """
        Создает объект и возвращает его объект.
        :param item: любой объект модели, который может быть добавлен в бд
        """
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def remove_item(self, id_item: int, Model: Any):
        item = self.get_current_item(id_item, Model).first()
        if item:
            self.session.delete(item)
            self.session.commit()

    def update_item(self, item_id: int, Model: Any,
                    data_to_update: BaseModel) -> Any:
        item = self.get_current_item(item_id, Model).first()
        for var, value in vars(data_to_update).items():
            setattr(item, var, value) if value else None
        self.create_item(item)
        return item

    def get_filtered_item(self, model: str, **kwargs) -> Any:
        query = self.session.query(model).filter_by(**kwargs).first()
        if query:
            return query
