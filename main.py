import asyncio
from pathlib import Path

from dou import DouGreaterThan2001Pdf, pdf_pipeline

TEST_CASES = ["001", "002", "003"]


async def main() -> None:
    pdfs = [
        DouGreaterThan2001Pdf(source=Path(f"docs/{case}/INPDFViewer.pdf"))
        for case in TEST_CASES
    ]
    await pdf_pipeline(pdfs)


if __name__ == "__main__":
    asyncio.run(main())
