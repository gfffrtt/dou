from dataclasses import dataclass

from dou.mask.config import MASK_BOTTOM, MASK_DPI, MASK_HEIGHT, MASK_WIDTH


@dataclass
class MaskPdfParams:
    width: float = MASK_WIDTH
    height: float = MASK_HEIGHT
    bottom: float = MASK_BOTTOM
    dpi: float = MASK_DPI
