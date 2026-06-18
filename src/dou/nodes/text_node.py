from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.nodes_list import NodesList


@dataclass
class TextNode:
    text: str
    kind: Literal["text"]
    level: int
    item: TextItem

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        return isinstance(item, TextItem)

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> TextNode:
        return cls(text=item.text, level=level, item=item, kind="text")
