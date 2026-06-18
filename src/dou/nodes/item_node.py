from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.alinea_node import AlineaNode
from dou.nodes.nodes_list import NodesList

ITEM_REGEX = re.compile(
    r"^(?P<number>\d+)\.\s*(?P<text>.*)$",
    re.DOTALL,
)


@dataclass
class ItemNode:
    kind: Literal["item"]
    level: int
    number: str
    text: str
    item: TextItem
    parent: AlineaNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        if context.get_last_alinea_node() is None:
            return False
        return ITEM_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> ItemNode:
        parent = context.get_last_alinea_node()
        assert parent is not None
        match = ITEM_REGEX.match(item.text.strip())
        assert match is not None
        return cls(
            kind="item",
            level=level,
            number=match.group("number"),
            text=match.group("text").strip(),
            item=item,
            parent=parent,
        )
