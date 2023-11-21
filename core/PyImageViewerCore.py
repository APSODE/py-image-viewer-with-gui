from typing import List, Optional
from Testor import ROOT_PATH
import os
from core.manager.ImageManager import ImageManager


class PyImageViewerCore:
    def __init__(self):
        self._image_manager: Optional[ImageManager] = None

    @staticmethod
    def create_core() -> "PyImageViewerCore":
        return PyImageViewerCore()

    @staticmethod
    def get_image_file_dirs() -> List[str]:
        return os.listdir(os.path.join(ROOT_PATH, "image_sources"))

    @staticmethod
    def get_image_file_dir(image_name: str):
        return os.path.join(ROOT_PATH, "image_sources", image_name)

    def create_manager(self, image_dir: str):
        self._image_manager = ImageManager.create_manager(image_dir = image_dir)

    @property
    def image_manager(self) -> ImageManager:
        return self._image_manager

    @image_manager.setter
    def image_manager(self, value: ImageManager):
        self._image_manager = value
