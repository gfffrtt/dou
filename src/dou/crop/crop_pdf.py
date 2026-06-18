import asyncio
from pathlib import Path

import pypdfium2 as pdfium

from dou.crop.crop_pdf_params import CropPdfParams


async def crop_pdf(
    pdf_path: str | Path,
    params: CropPdfParams | None = None,
) -> Path:
    params = params or CropPdfParams()

    def run() -> Path:
        path = Path(pdf_path).resolve()
        output = path.with_name(f"{path.stem}-cropped{path.suffix}")

        top_pt = params.top * 72 / params.dpi
        left_pt = params.left * 72 / params.dpi
        bottom_pt = params.bottom * 72 / params.dpi
        right_pt = params.right * 72 / params.dpi

        pdf = pdfium.PdfDocument(str(path))
        try:
            for page_index in range(len(pdf)):
                page = pdf[page_index]
                box_left, box_bottom, box_right, box_top = page.get_mediabox()

                new_left = box_left + left_pt
                new_bottom = box_bottom + bottom_pt
                new_right = box_right - right_pt
                new_top = box_top - top_pt

                if new_left >= new_right or new_bottom >= new_top:
                    raise ValueError(
                        f"Crop margins are too large for page {page_index + 1}: "
                        f"top={params.top}, left={params.left}, bottom={params.bottom}, right={params.right}"
                    )

                crop_box = (new_left, new_bottom, new_right, new_top)
                page.set_cropbox(*crop_box)
                page.set_mediabox(*crop_box)
                page.set_trimbox(*crop_box)

            pdf.save(str(output))
        finally:
            pdf.close()

        return output

    return await asyncio.to_thread(run)
