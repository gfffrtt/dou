from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TableItem

from dou.nodes.nodes_list import NodesList


@dataclass
class TableNode:
    kind: Literal["table"]
    level: int
    item: TableItem

    @property
    def text(self) -> str:
        return type(self.item.data.grid)

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        return isinstance(item, TableItem)

    @classmethod
    def from_item(cls, item: TableItem, level: int, context: NodesList) -> TableNode:
        return cls(level=level, item=item, kind="table")
