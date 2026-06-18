from dataclasses import dataclass

from dou.crop.config import CROP_BOTTOM, CROP_DPI, CROP_LEFT, CROP_RIGHT, CROP_TOP


@dataclass
class CropPdfParams:
    top: float = CROP_TOP
    left: float = CROP_LEFT
    bottom: float = CROP_BOTTOM
    right: float = CROP_RIGHT
    dpi: float = CROP_DPI
