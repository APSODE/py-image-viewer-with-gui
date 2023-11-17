from typing import Tuple, Union, Literal, Type
from numpy import ndarray

PIXEL_TYPE = Union[Tuple[int, int, int], int, ndarray]
CHANNEL_TYPE_LITERAL = Literal["RGB", "YUV", "GRAY"]
CHANNEL_NAME_LITERAL = Literal["RGB", "YCbCr", "L"]
CHANNEL_LITERAL = Literal["R", "G", "B", "Y", "U", "V", "L"]
CONVERT_TYPE = Literal["YUV", "GRAY"]
ROTATE_TYPE = Literal["vertical", "horizontal"]
SPLITABLE_CHANNEL_TYPE_LITERAL = Literal["RGB", "YUV"]
