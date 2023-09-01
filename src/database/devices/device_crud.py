from typing import Optional

from src.database.base.base_crud import BaseCrud
from src.database.devices.device_model import Device
from src.database.shemas import DeviceItem


class DeviceCrud(BaseCrud):
    @property
    def device_names(self) -> list[str]:
        return [i.name for i in self.get_all_devices_images()]

    def get_all_devices_images(self) -> list[Device]:
        return self.get_all_items(Device)

    def get_device_by_name(self, device_name) -> Optional[Device | None]:
        query = self.session.query(Device).filter(
            Device.name == device_name
        ).first()
        return query

    def create_new_device(self, data_to_save: list[DeviceItem]) -> Device:
        device = data_to_save[0]
        query = self.session.query(Device).filter(
            Device.name == device.name
        ).first()
        if not query:
            new_device = Device(
                name=device.name,
                description=device.description,
                price=device.price,
            )
            return self.create_item(new_device)
        return query


DeviceCr = DeviceCrud()
