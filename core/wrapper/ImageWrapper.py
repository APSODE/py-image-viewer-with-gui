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
        # 해당 메소드의 각 convert메소드는 기본 내장 convert메소드를 제외하면 변환 타입별 약 10초 가량 소요됨
        # 해당 메소드의 실행 시간을 줄이려면, 멀티스레딩을 사용하는 것이 최선으로 보여짐
        # 해당 메소드에서 사용되는 convert메소드들은 해당 객체가 필수적으로 필요로하는 Image객체를 생성하므로
        # 비동기 방식으로는 블로킹을 막을수 없는 것으로 예상됨
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





