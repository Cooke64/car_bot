from typing import Optional

from src.database.base.base_crud import BaseCrud
from src.database.devices.device_model import Device
from src.database.images.image_model import DeviceImages, DoneJobImages
from src.states.add_media import AddMediaShema, MediaFile
from src.states.order_state import MediaMesTypes


class ImageCrud(BaseCrud):
    def get_all_devices_images(self) -> list[DeviceImages]:
        return self.get_all_items(DeviceImages)

    def get_done_job_images(self) -> list[DoneJobImages]:
        return self.get_all_items(DoneJobImages)

    def get_photo_device(self, photo_id: str) -> DeviceImages:
        return self.session.query(DeviceImages).filter(
            DeviceImages.photo_id == photo_id
        ).first()

    def get_photo(self, unique_id: str) -> DeviceImages:
        return self.session.query(DeviceImages).filter(
            DeviceImages.file_unique_id == unique_id
        ).first()

    def get_photo_done_jobe(self, photo_id: str) -> DoneJobImages:
        return self.session.query(DoneJobImages).filter(
            DoneJobImages.photo_id == photo_id
        ).first()

    @staticmethod
    def __get_media_data(media_file: MediaFile) -> tuple[str, str]:
        return media_file.file_unique_id, media_file.photo_id

    def __save_device(self, photo_data: AddMediaShema, device_id: int):
        """Сохраняет изображение представленных медиапродукта с описанием."""
        file_unique_id, photo_id = self.__get_media_data(photo_data.medai_file)
        photo: DeviceImages = self.get_photo_device(photo_id)
        if not photo or self.get_current_item(device_id, Device):
            new_instanse = DeviceImages(
                file_unique_id=file_unique_id,
                photo_id=photo_id,
                device_id=device_id,
                description=photo_data.description
            )
            self.create_item(new_instanse)
            return
        photo.description = photo_data.description
        self.session.commit()

    def __save_doobe_job(self, photo_data: AddMediaShema):
        """Сохраняет изображение готовых работ с описанием."""
        file_unique_id, photo_id = self.__get_media_data(photo_data.medai_file)
        photo = self.get_photo_done_jobe(photo_id)
        if not photo:
            new_instanse = DoneJobImages(
                file_unique_id=file_unique_id,
                photo_id=photo_id,
                description=photo_data.description
            )
            self.create_item(new_instanse)
            return
        photo.description = photo_data.description
        self.session.commit()

    def add_photo_in_db(
            self,
            photo_data: AddMediaShema, device_id: Optional[int] = None
    ) -> None:
        if photo_data.media_type == MediaMesTypes.devices.value:
            self.__save_device(photo_data, device_id)
        else:
            self.__save_doobe_job(photo_data)

    def remove_done_job(self, unique_id: str):
        item = self.get_photo_done_jobe(unique_id)
        if item:
            self.session.delete(item)
            self.session.commit()

    def remove_device(self, unique_id: str):
        item = self.get_photo_device(unique_id)
        if item:
            self.session.delete(item)
            self.session.commit()


Images = ImageCrud()
