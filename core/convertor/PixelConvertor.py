from typing import Dict, Optional, Tuple, Literal
from core.type_annotation.CustomTypes import PIXEL_TYPE, CHANNEL_TYPE_LITERAL, CHANNEL_LITERAL, CONVERT_TYPE


class PixelConvertor:
    @staticmethod
    def calc_pixel_data(original_pixel_data: PIXEL_TYPE,
                        channel_type: CHANNEL_TYPE_LITERAL,
                        channel: Optional[CHANNEL_LITERAL | str] = None) -> int:

        if channel_type == "RGB" and channel is not None:
            return original_pixel_data[channel_type.index(channel)]

        if channel_type == "YUV" and channel is not None:
            return PixelConvertor._convert_rgb_to_yuv(rgb_pixel_data = original_pixel_data, selected_channel = channel)

        if channel_type == "GRAY":
            return PixelConvertor._convert_rgb_to_gray(rgb_pixel_data = original_pixel_data)

    @staticmethod
    def calc_full_pixel_data(original_pixel_data: PIXEL_TYPE,
                             channel_type: CONVERT_TYPE) -> PIXEL_TYPE:

        if channel_type == "RGB":
            return original_pixel_data

        if channel_type == "YUV":
            converted_pixel = (
                PixelConvertor._convert_rgb_to_yuv(original_pixel_data, "Y"),
                PixelConvertor._convert_rgb_to_yuv(original_pixel_data, "U"),
                PixelConvertor._convert_rgb_to_yuv(original_pixel_data, "V")
            )

            return converted_pixel

        if channel_type == "GRAY":
            return PixelConvertor._convert_rgb_to_gray(original_pixel_data)

    @staticmethod
    def _convert_rgb_to_yuv(rgb_pixel_data: Tuple[int, int, int], selected_channel: Literal["Y", "U", "V"]) -> int:
        yuv_const_data: Dict[Literal["Y", "U", "V"], Tuple[float, float, float]] = {
            "Y": (0.299, 0.587, 0.114),
            "U": (-0.14713, -0.288862, 0.436),
            "V": (0.615, -0.51498, -0.10001)
        }

        # int(pixel[R / G / B] * YUV_const[R / G / B]) RGB에 대한 최종 연산값을 다 더하면
        # 입력받은 selected_channel에 따른 Y/U/V 채널의 결과값이 반환된다
        return int(
            sum([rgb_pixel * yuv_const_data.get(selected_channel)[idx] for idx, rgb_pixel in enumerate(rgb_pixel_data)])
        )

    @staticmethod
    def _convert_rgb_to_gray(rgb_pixel_data: Tuple[int, int, int]) -> int:
        grayscale_const_data: Tuple[float, float, float] = (0.299, 0.587, 0.114)
        return int(sum([grayscale_const_data[idx] * rgb_pixel for idx, rgb_pixel in enumerate(rgb_pixel_data)]))
