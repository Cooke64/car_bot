from typing import Optional

from src.bot.database.base.base_crud import BaseCrud
from src.bot.database.devices.device_model import Device


class DeviceCrud(BaseCrud):
    def get_all_devices_images(self) -> list[Device]:
        return self.get_all_items(Device)

    def get_device_by_name(self, device_name) -> Optional[Device | None]:
        query = self.session.query(Device).filter(
            Device.name == device_name
        ).first()
        return query


DeviceCr = DeviceCrud()
