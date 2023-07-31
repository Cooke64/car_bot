from src.bot.database.base.base_crud import BaseCrud
from src.bot.database.car_service.car_service_model import CarBrend, Model
from src.bot.database.shemas import  OrderShema
from src.bot.database.user_order.user_order_model import UserOrders, Order
from src.bot.states.order_state import UserOrderData


class UserOrderCrud(BaseCrud):

    def get_model(self, model_name: str) -> Model:
        query = self.session.query(Model).join(CarBrend).filter(
            Model.name == model_name
        ).first()
        if query:
            return query

    def create_user_order(self, order: OrderShema):
        new_order = Order(**order.dict())
        created = self.create_item(new_order)
        print(created)

    def get_orders(self) -> list[Order]:
        return self.get_all_items(Order)


UserOrder = UserOrderCrud()
