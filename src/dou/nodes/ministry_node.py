from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, SectionHeaderItem

from dou.nodes.ministries import MINISTRIES
from dou.nodes.nodes_list import NodesList
from dou.nodes.section_header_node import SectionHeaderNode


@dataclass
class MinistryNode:
    kind: Literal["ministry"]
    level: int
    text: str
    item: SectionHeaderNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        return (
            isinstance(item, SectionHeaderItem)
            and item.text.strip() in MINISTRIES
        )

    @classmethod
    def from_item(
        cls, item: SectionHeaderItem, level: int, context: NodesList
    ) -> MinistryNode:
        header = SectionHeaderNode.from_item(item, level, context)
        return cls(text=item.text, level=level, item=header, kind="ministry")
