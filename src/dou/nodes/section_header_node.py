from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, SectionHeaderItem

from dou.nodes.nodes_list import NodesList


@dataclass
class SectionHeaderNode:
    kind: Literal["section_header"]
    level: int
    text: str
    item: SectionHeaderItem

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        return isinstance(item, SectionHeaderItem)

    @classmethod
    def from_item(
        cls, item: SectionHeaderItem, level: int, context: NodesList
    ) -> SectionHeaderNode:
        return cls(text=item.text, level=level, item=item, kind="section_header")
