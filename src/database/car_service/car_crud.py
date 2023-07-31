from sqlalchemy.orm import joinedload

from src.bot.database.base.base_crud import BaseCrud
from src.bot.database.car_service.car_service_model import (
    CarBrend,
    Model,
    BrendModelShema
)


class CarCrud(BaseCrud):
    def get_all_brends(self) -> list[CarBrend]:
        return self.session.query(CarBrend).options(
            joinedload(CarBrend.models)).all()

    def get_avaible_models(self):
        return [model.name for model in self.get_all_items(Model)]

    def get_brand_models(self, brand_name) -> list[Model]:
        query: CarBrend = self.session.query(CarBrend).options(
            joinedload(CarBrend.models)).filter(
                CarBrend.name == brand_name
            ).first()
        return query.models

    def get_brand_by_name(self, brand_name) -> CarBrend:
        query = self.session.query(CarBrend).filter(
            CarBrend.name == brand_name
        ).first()
        return query

    def get_model_by_name(self, model_name):
        query = self.session.query(Model).filter(
            Model.name == model_name
        ).first()
        return query

    def __create_new_brand(self, brand_name: str, coef: str) -> CarBrend:
        brand = self.get_brand_by_name(brand_name)
        if not brand:
            new_brend = CarBrend(name=brand_name, car_coef=coef)
            return self.create_item(new_brend)
        return brand

    def __create_model(self, model_name, model_coef, car_brend_id):
        model = self.get_model_by_name(model_name)
        if not model:
            model = Model(
                name=model_name.capitalize(), model_coef=model_coef,
                car_brend_id=car_brend_id
            )
            return self.create_item(model)
        return model

    def create_auto(self, auto_data: BrendModelShema):
        brand = self.__create_new_brand(auto_data.brend_name,
                                        auto_data.brend_coef)
        self.__create_model(
            auto_data.model_name.capitalize(), auto_data.brend_coef, brand.id
        )
        print('created')


car_crud = CarCrud()
