from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.article_node import ArticleNode
from dou.nodes.nodes_list import NodesList
from dou.nodes.paragraph_node import ParagraphNode

INCISO_REGEX = re.compile(
    r"^(?P<roman>[IVXLCDM]+)\s*[-–—]\s*(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class IncisoNode:
    kind: Literal["inciso"]
    level: int
    roman: str
    text: str
    item: TextItem
    parent: ArticleNode | ParagraphNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        if context.get_inciso_parent() is None:
            return False
        return INCISO_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> IncisoNode:
        parent = context.get_inciso_parent()
        assert parent is not None
        match = INCISO_REGEX.match(item.text.strip())
        assert match is not None
        return cls(
            kind="inciso",
            level=level,
            roman=match.group("roman").upper(),
            text=match.group("text").strip(),
            item=item,
            parent=parent,
        )
