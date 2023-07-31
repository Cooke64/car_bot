from src.bot.database.base.base_crud import BaseCrud
from src.bot.database.images.image_model import DeviceImages, DoneJobImages
from src.bot.states.add_media import AddMediaShema, MediaFile
from src.bot.states.order_state import MediaMesTypes


class ImageCrud(BaseCrud):
    def get_all_devices_images(self) -> list[DeviceImages]:
        return self.get_all_items(DeviceImages)

    def get_done_job_images(self) -> list[DoneJobImages]:
        return self.get_all_items(DoneJobImages)

    def get_photo_device(self, file_unique_id: str) -> DeviceImages:
        return self.session.query(DeviceImages).filter(
            DeviceImages.file_unique_id == file_unique_id
        ).first()

    def get_photo_done_jobe(self, file_unique_id: str) -> DoneJobImages:
        return self.session.query(DoneJobImages).filter(
            DoneJobImages.file_unique_id == file_unique_id
        ).first()

    @staticmethod
    def __get_media_data(media_file: MediaFile) -> tuple[str, str]:
        return media_file.file_unique_id, media_file.photo_id

    def add_photo_in_db(
            self,
            photo_data: AddMediaShema
    ) -> None:
        file_unique_id, photo_id = self.__get_media_data(photo_data.medai_file)
        if photo_data.media_type == MediaMesTypes.devices.value:
            photo: DeviceImages = self.get_photo_device(file_unique_id)
            if not photo:
                new_instanse = DeviceImages(
                    file_unique_id=file_unique_id,
                    photo_id=photo_id,
                    description=photo_data.description
                )
                self.create_item(new_instanse)
                return
            photo.description = photo_data.description
            self.session.commit()
        else:
            photo = self.get_photo_done_jobe(file_unique_id)
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

    def remove_done_job(self, unique_id):
        item = self.get_photo_done_jobe(unique_id)
        if item:
            self.session.delete(item)
            self.session.commit()

    def remove_device(self, unique_id):
        item = self.get_photo_device(unique_id)
        if item:
            self.session.delete(item)
            self.session.commit()


Images = ImageCrud()
