from typing import Optional, Tuple
from PIL.Image import Image
from PIL.Image import open as img_open

from core.convertor.ImageConvertor import ImageConvertor
from core.custom_decorator.RuntimeCounter import RuntimeCounter


class ImageWrapper(Image):
    def __init__(self, image_dir: str, with_base_convertor: bool, with_optimized_convertor: bool):
        self._original_image = img_open(image_dir)
        self._resize_image()
        self._rgb_image: Optional[Image] = None
        self._yuv_image: Optional[Image] = None
        self._gray_image: Optional[Image] = None
        self._set_all_channel_image(with_base_convertor, with_optimized_convertor)

    @staticmethod
    def create_object(image_dir: str, with_base_convertor: bool, with_optimized_convertor) -> "ImageWrapper":
        return ImageWrapper(image_dir, with_base_convertor, with_optimized_convertor)

    def _resize_image(self):
        original_width, original_height = self._original_image.size
        resized_size: Optional[Tuple[int, int]] = None

        if original_width * original_height <= 1920*1080:
            return None  # Full HD 해상도의 픽셀 갯수보다 적을경우 리사이징이 필요 없음.

        if self._original_image.width > 1920:
            resized_width = 1920
            resized_height = int((1920 / original_width) * original_height)
            resized_size = (resized_width, resized_height)

        if self._original_image.height > 1080:
            resized_height = 1080
            resized_width = int((1080 / original_height) * original_width)
            resized_size = (resized_width, resized_height)

        if resized_size is not None:
            self._original_image = self._original_image.resize(resized_size)

    @RuntimeCounter("ImageWrapper all channel image convert")
    def _set_all_channel_image(self, with_base_convertor: bool, with_optimized_convertor: bool):
        if with_base_convertor:
            self._rgb_image = self._original_image.convert("RGB")
            self._yuv_image = self._original_image.convert("YCbCr")
            self._gray_image = self._original_image.convert("L")

        elif with_optimized_convertor:
            self._rgb_image = self._original_image
            self._yuv_image = ImageConvertor.optimized_convert(self, "YUV")
            self._gray_image = ImageConvertor.optimized_convert(self, "GRAY")

        else:
            self._rgb_image = self._original_image
            self._yuv_image = ImageConvertor.convert(self, "YUV")
            self._gray_image = ImageConvertor.convert(self, "GRAY")

    @property
    def original_image(self) -> Image:
        return self._original_image

    @property
    def rgb_image(self):
        return self._rgb_image

    @property
    def yuv_image(self):
        return self._yuv_image

    @property
    def gray_image(self):
        return self._gray_image





