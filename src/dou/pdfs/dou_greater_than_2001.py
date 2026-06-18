from dataclasses import dataclass, field
from pathlib import Path

from dou.crop.crop_pdf_params import CropPdfParams
from dou.mask.mask_pdf_params import MaskPdfParams


@dataclass
class DouGreaterThan2001Pdf:
    source: Path
    crop_params: CropPdfParams = field(
        default_factory=lambda: CropPdfParams(top=70, left=60, bottom=67, right=60)
    )
    mask_params: MaskPdfParams = field(
        default_factory=lambda: MaskPdfParams(width=20, height=3)
    )
