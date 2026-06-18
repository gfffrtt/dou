from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, ListItem

from dou.nodes.nodes_list import NodesList


@dataclass
class ListNode:
    kind: Literal["list"]
    level: int
    item: ListItem

    @property
    def text(self) -> str:
        return self.item.text

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        return isinstance(item, ListItem)

    @classmethod
    def from_item(cls, item: ListItem, level: int, context: NodesList) -> ListNode:
        return cls(level=level, item=item, kind="list")
