import asyncio
from pathlib import Path

import fitz

from dou.mask.mask_pdf_params import MaskPdfParams


async def mask_pdf(
    pdf_path: str | Path,
    params: MaskPdfParams | None = None,
) -> Path:
    params = params or MaskPdfParams()

    def run() -> Path:
        path = Path(pdf_path).resolve()
        output = path.with_name(f"{path.stem}-masked{path.suffix}")

        width_pt = params.width * 72 / params.dpi
        height_pt = params.height * 72 / params.dpi
        bottom_pt = params.bottom * 72 / params.dpi

        pdf = fitz.open(str(path))
        try:
            for page in pdf:
                page_rect = page.rect
                x0 = (page_rect.width - width_pt) / 2
                x1 = x0 + width_pt
                y1 = page_rect.height - bottom_pt
                y0 = y1 - height_pt

                rect = fitz.Rect(x0, y0, x1, y1)
                page.add_redact_annot(rect, fill=(1, 1, 1))
                page.apply_redactions()

            pdf.save(str(output))
        finally:
            pdf.close()

        return output

    return await asyncio.to_thread(run)
