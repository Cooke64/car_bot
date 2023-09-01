from typing import Optional

from sqlalchemy.orm import joinedload

from src.database.base.base_crud import BaseCrud
from src.database.car_service.car_service_model import (
    CarBrend,
    Model,
    BrendModelShema
)
from src.database.shemas import Brand
from functools import lru_cache


class CarCrud(BaseCrud):

    @property
    @lru_cache()
    def brands_names(self) -> list[str]:
        """Возвращает список названий всех брендов. Возвращает список названий в строковм виде."""
        return [brand.name for brand in self.get_all_brends()]

    @lru_cache()
    def get_models_names(self, brand_name: str) -> Optional[list[str]]:
        """Возвращает список названий модели в бренде. Возвращает список названий в строковм виде."""
        if self.get_brand_models(brand_name):
            return [model.name for model in self.get_brand_models(brand_name)]
        return None

    def get_all_brends(self) -> list[CarBrend]:
        return self.session.query(CarBrend).options(
            joinedload(CarBrend.models)).all()

    def get_brand_models(self, brand_name: str) -> list[Model]:
        query: CarBrend = self.session.query(CarBrend).options(
            joinedload(CarBrend.models)).filter(
                CarBrend.name == brand_name
            ).first()
        if query:
            return query.models

    def get_brand_by_name(self, brand_name) -> CarBrend:
        return self.session.query(CarBrend).filter(
            CarBrend.name == brand_name
        ).first()

    def get_model_by_name(self, model_name: str) -> Model:
        return self.session.query(Model).filter(
            Model.name == model_name
        ).first()

    def __create_new_brand(self, brand_name: str, coef: float) -> CarBrend:
        brand = self.get_brand_by_name(brand_name)
        if not brand:
            new_brend = CarBrend(name=brand_name.capitalize(), car_coef=coef)
            return self.create_item(new_brend)
        return brand

    def __create_model(self, model_name, model_coef, car_brend_id):
        model = self.get_model_by_name(model_name)
        if not model:
            model = Model(
                name=model_name.capitalize(), coef=model_coef,
                car_brend_id=car_brend_id
            )
            return self.create_item(model)
        return model

    def create_auto(self, auto_data: BrendModelShema):
        brand = self.__create_new_brand(
            auto_data.brend_name, auto_data.brend_coef)
        self.__create_model(
            auto_data.model_name.capitalize(), auto_data.brend_coef, brand.id
        )

    def create_brand_models(self, brend: Brand):
        new_brand = self.__create_new_brand(brend.brand_name, brend.brand_coef)
        for model in brend.models:
            self.__create_model(
                model.model_name, model.model_coef, new_brand.id
            )


car_crud = CarCrud()
