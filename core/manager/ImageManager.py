from typing import Dict, List, Tuple
from core.custom_decorator.RuntimeCounter import RuntimeCounter
from core.type_annotation.CustomTypes import CHANNEL_TYPE_LITERAL, CHANNEL_LITERAL, ROTATE_TYPE, PIXEL_TYPE
from core.wrapper.ImageWrapper import ImageWrapper
from PIL.Image import Image, fromarray
from PIL.Image import new as new_image

import os.path
import numpy as np


class ImageManager:
    def __init__(self, image_dir: str, with_base_convertor: bool = False, with_optimized_convertor: bool = False):
        self._image_wrapper = ImageWrapper.create_object(image_dir, with_base_convertor, with_optimized_convertor)
        self._loaded_image = self._image_wrapper.original_image
        self._channel_amount_data: Dict[CHANNEL_TYPE_LITERAL, int] = {
            "RGB": 3,
            "YUV": 3,
            "GRAY": 1
        }

    @staticmethod
    def create_manager(image_dir: str) -> "ImageManager":
        return ImageManager(image_dir)

    @staticmethod
    def save_image(file_name: str, image: Image):
        from Testor import ROOT_PATH
        image.save(os.path.join(ROOT_PATH, "converted_images", file_name))

    @RuntimeCounter("Non-Optimized Image Split")
    def image_split_by_channel(self, channel_type: CHANNEL_TYPE_LITERAL):
        target_image: Image = getattr(self._image_wrapper, f"{channel_type.lower()}_image")
        channel_images: List[Image]
        channel_images = [new_image("L", target_image.size) for _ in range(self.get_channel_amount(channel_type))]
        print(f"{channel_type} image split start!")
        print(f"width : {target_image.width}\n"
              f"height : {target_image.height}\n"
              f"total : {target_image.width * target_image.height}"
              )
        # 반복문 실행횟수 최대 -> 3 * 1080 * 1920 = 6220800
        for channel_idx in range(self.get_channel_amount(channel_type)):  # 1 or 3
            for y_pos in range(target_image.height):  # 최대값 1080
                for x_pos in range(target_image.width):  # 최대값 1920
                    channel_images[channel_idx].putpixel(
                        (x_pos, y_pos),
                        self._get_split_pixel_data(
                            target_pixel_data = target_image.getpixel((x_pos, y_pos)),
                            channel_type = channel_type,
                            channel_idx = channel_idx
                        )
                    )

            self.save_image(
                f"{channel_type}_channel_split_image_{channel_idx}.jpg",
                channel_images[channel_idx]
            )

    @RuntimeCounter("Optimized Image Split")
    def optimized_image_split_by_channel(self, channel_type: CHANNEL_TYPE_LITERAL):
        target_image: Image = getattr(self._image_wrapper, f"{channel_type.lower()}_image")
        channel_images: List[Image]
        channel_images = [new_image("L", target_image.size) for _ in range(self.get_channel_amount(channel_type))]
        print(f"{channel_type} image split start!")
        print(f"width : {target_image.width}\n"
              f"height : {target_image.height}\n"
              f"total : {target_image.width * target_image.height}"
              )

        # NumPy array로 변환
        target_data = np.array(target_image)

        for channel_idx in range(self.get_channel_amount(channel_type)):
            channel_images[channel_idx].putdata(
                [
                    self._get_split_pixel_data(
                        target_pixel_data = target_data[y_pos, x_pos],
                        channel_type = channel_type,
                        channel_idx = channel_idx
                    )
                    for y_pos in range(target_image.height)
                    for x_pos in range(target_image.width)
                ]
            )

            self.save_image(
                f"{channel_type}_channel_split_image_{channel_idx}_optimized.jpg",
                channel_images[channel_idx]
            )

    @RuntimeCounter("Non-Optimzed Image Rotate")
    def rotate_image(self, rotate_type: ROTATE_TYPE):
        rotated_image = new_image("RGB", self._loaded_image.size)
        width, height = self._loaded_image.size
        # rotate_range_param = self._create_rotate_range_param(rotate_type = rotate_type)

        for y_pos in range(height):
            for x_pos in range(width):
                rotated_image.putpixel(
                    self._create_rotate_pos(rotate_type = rotate_type, current_pos = (x_pos, y_pos)),
                    self._loaded_image.getpixel((x_pos, y_pos))
                )

        self.save_image(f"{rotate_type}_rotated_image.jpg", rotated_image)

    @RuntimeCounter("Optimized Image Rotate")
    def optimized_rotate_image(self, rotate_type: ROTATE_TYPE):
        rotated_image = new_image("RGB", self._loaded_image.size)
        width, height = self._loaded_image.size

        rotated_image.putdata(
            [
                self._loaded_image.getpixel(self._create_rotate_pos(rotate_type, (x_pos, y_pos)))
                for y_pos in range(height)
                for x_pos in range(width)
            ]
        )

        return rotated_image

    @RuntimeCounter("Center Position 50% Crop Image")
    def crop_image(self):
        target_data = np.array(self._loaded_image)
        width, height = self._loaded_image.size
        crop_size = int(min(width, height) * 0.25)

        crroped_image_array = target_data[
            height // 2 - crop_size: height // 2 + crop_size,
            width // 2 - crop_size: width // 2 + crop_size
        ]

        self.save_image(f"center_position_50%_crop_image.jpg", fromarray(crroped_image_array))

    def get_channel_amount(self, channel_type: CHANNEL_TYPE_LITERAL) -> int:
        return self._channel_amount_data.get(channel_type)

    def _create_rotate_range_param(self, rotate_type: ROTATE_TYPE) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        width, height = self._loaded_image.size
        rotate_operator = (-1, 1) if rotate_type == "vertical" else (1, -1)
        y_pos_range_param: Tuple[int, int, int]
        x_pos_range_param: Tuple[int, int, int]

        if rotate_type == "vertical":
            y_pos_range_param = (height - 1, -1, rotate_operator[0])
            x_pos_range_param = (0, width, rotate_operator[1])
        else:
            y_pos_range_param = (0, height, rotate_operator[0])
            x_pos_range_param = (width - 1, -1, rotate_operator[1])

        return y_pos_range_param, x_pos_range_param

    def _create_rotate_pos(self, rotate_type: ROTATE_TYPE, current_pos: Tuple[int, int]) -> Tuple[int, int]:
        width, height = self._loaded_image.size

        if rotate_type == "vertical":
            return current_pos[0], ((height - 1) - current_pos[1])
        else:
            return ((width - 1) - current_pos[0]), current_pos[1]

    @staticmethod
    def _get_split_pixel_data(target_pixel_data: PIXEL_TYPE,
                              channel_type: CHANNEL_TYPE_LITERAL,
                              channel_idx: int) -> PIXEL_TYPE:

        if channel_type in ["RGB", "YUV"]:
            return target_pixel_data[channel_idx]

        else:
            return target_pixel_data
