from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import (
    TextItem,
    TableItem,
    SectionHeaderItem,
    ListItem,
)
from pathlib import Path


async def nodes(
    pdf_path: str | Path,
):
    converter = DocumentConverter()
    doc = converter.convert(pdf_path).document
    for item, _ in doc.iterate_items():
        if isinstance(item, TextItem):
            print(item.text)
        elif isinstance(item, TableItem):
            print(item.data.model_dump_json())
        elif isinstance(item, SectionHeaderItem):
            print(item.text)
        elif isinstance(item, ListItem):
            print(item.text)
