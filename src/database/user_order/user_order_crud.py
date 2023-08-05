from src.database.base.base_crud import BaseCrud
from src.database.car_service.car_service_model import CarBrend, Model
from src.database.shemas import OrderShema
from src.database.user_order.user_order_model import Order
from src.handlers.users.utils.user_order_service import get_result_message
from src.states.order_state import UserOrderData


class UserOrderCrud(BaseCrud):

    def get_model(self, model_name: str) -> Model:
        query = self.session.query(Model).join(CarBrend).filter(
            Model.name == model_name
        ).first()
        if query:
            return query

    def create_user_order(self, order: OrderShema | UserOrderData):
        if isinstance(order, UserOrderData):
            new_order = Order(username=order.name,
                              phone=order.phone_number,
                              order=get_result_message(order)
                              )
        else:
            new_order = Order(username=order.username,
                              phone=order.phone,
                              order=order.order
                              )
        self.create_item(new_order)

    def get_orders(self) -> list[Order]:
        return self.get_all_items(Order)


UserOrder = UserOrderCrud()
