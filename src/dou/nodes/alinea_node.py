from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.inciso_node import IncisoNode
from dou.nodes.nodes_list import NodesList

ALINEA_REGEX = re.compile(
    r"^(?P<letter>[a-z])\)\s*(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class AlineaNode:
    kind: Literal["alinea"]
    level: int
    letter: str
    text: str
    item: TextItem
    parent: IncisoNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        if context.get_last_inciso_node() is None:
            return False
        return ALINEA_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> AlineaNode:
        parent = context.get_last_inciso_node()
        assert parent is not None
        match = ALINEA_REGEX.match(item.text.strip())
        assert match is not None
        return cls(
            kind="alinea",
            level=level,
            letter=match.group("letter").lower(),
            text=match.group("text").strip(),
            item=item,
            parent=parent,
        )
