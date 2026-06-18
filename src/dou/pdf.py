from pathlib import Path
from typing import Protocol

from dou.crop.crop_pdf_params import CropPdfParams
from dou.mask.mask_pdf_params import MaskPdfParams


class Pdf(Protocol):
    source: Path
    crop_params: CropPdfParams
    mask_params: MaskPdfParams
