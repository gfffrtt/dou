# dou

PDF crop and mask pipeline for DOU documents.

## Install

```bash
pip install -e .
```

## Usage

```python
import asyncio
from pathlib import Path

from dou import DouViewerPdf, pdf_pipeline

async def main() -> None:
    pdfs = [
        DouViewerPdf(source=Path("docs/001/INPDFViewer.pdf")),
    ]
    outputs = await pdf_pipeline(pdfs)
    print(outputs)

asyncio.run(main())
```

Or run the sample entry point:

```bash
python main.py
```

## Adding strategies

Implement a class with `source`, `crop_params`, and `mask_params` attributes (see `DouViewerPdf` in `src/dou/pdfs/dou_viewer.py`). Pass instances to `pdf_pipeline` — no changes to the pipeline are required.
