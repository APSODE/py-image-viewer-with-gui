from typing import Dict, TYPE_CHECKING
from core.convertor.PixelConvertor import PixelConvertor
from core.type_annotation.CustomTypes import CHANNEL_TYPE_LITERAL, CONVERT_TYPE, CHANNEL_NAME_LITERAL
from PIL.Image import new as new_image
from PIL.Image import Image
import numpy as np

if TYPE_CHECKING:
    from core.wrapper.ImageWrapper import ImageWrapper


_channel_amount_data: Dict[CHANNEL_TYPE_LITERAL, int] = {
    "RGB": 3,
    "YUV": 3,
    "GRAY": 1
}
_channel_name_data: Dict[CHANNEL_TYPE_LITERAL, CHANNEL_NAME_LITERAL] = {
    "RGB": "RGB",
    "YUV": "YCbCr",
    "GRAY": "L"
}


class ImageConvertor:
    @staticmethod
    def convert(target_image: "ImageWrapper", convert_type: CONVERT_TYPE) -> Image:
        converted_image = new_image(ImageConvertor._get_channel_name(convert_type), target_image.original_image.size)

        for y_pos in range(target_image.original_image.height):
            for x_pos in range(target_image.original_image.width):
                original_pixel = target_image.original_image.getpixel((x_pos, y_pos))

                converted_image.putpixel(
                    (x_pos, y_pos),
                    PixelConvertor.calc_full_pixel_data(
                        original_pixel_data = original_pixel,
                        channel_type = convert_type
                    )
                )

        return converted_image

    @staticmethod
    def optimized_convert(target_image: "ImageWrapper", convert_type: CONVERT_TYPE) -> Image:
        channel_name = ImageConvertor._get_channel_name(convert_type)
        converted_image = new_image(channel_name, target_image.original_image.size)

        # NumPy array로 변환
        target_data = np.array(target_image.original_image)

        converted_image.putdata(
            [
                PixelConvertor.calc_full_pixel_data(
                    original_pixel_data = target_data[y_pos, x_pos],
                    channel_type = convert_type
                )
                for y_pos in range(target_image.original_image.height)
                for x_pos in range(target_image.original_image.width)
            ]
        )

        return converted_image

    @staticmethod
    def _get_channel_name(channel_type: CHANNEL_TYPE_LITERAL) -> CHANNEL_NAME_LITERAL:
        return _channel_name_data.get(channel_type)
