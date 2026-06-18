from collections.abc import Sequence

from dou.crop.crop_pdf import crop_pdf
from dou.mask.mask_pdf import mask_pdf
from dou.pdf import Pdf
from dou.nodes import nodes


async def pdf_pipeline(pdfs: Sequence[Pdf]) -> None:
    for pdf in pdfs:
        cropped = await crop_pdf(pdf.source, pdf.crop_params)
        masked = await mask_pdf(cropped, pdf.mask_params)
        nodes_list = await nodes(masked)
        for node in nodes_list.nodes:
            print(f"<{node.kind}>")
            print(node.text)
            print(f"</{node.kind}>")
