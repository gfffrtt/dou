from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.article_node import ArticleNode
from dou.nodes.nodes_list import NodesList

PARAGRAPH_REGEX = re.compile(
    r"^§\s*(?P<number>\d+)[º°oO]\s*(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)
PARAGRAPH_UNIQUE_REGEX = re.compile(
    r"^Par[áa]grafo\s+[uú]nico\.?\s*(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class ParagraphNode:
    kind: Literal["paragraph"]
    level: int
    number: str | None
    is_unique: bool
    text: str
    item: TextItem
    parent: ArticleNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        if context.get_last_article_node() is None:
            return False
        text = item.text.strip()
        return (
            PARAGRAPH_REGEX.match(text) is not None
            or PARAGRAPH_UNIQUE_REGEX.match(text) is not None
        )

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> ParagraphNode:
        parent = context.get_last_article_node()
        assert parent is not None
        text = item.text.strip()
        unique_match = PARAGRAPH_UNIQUE_REGEX.match(text)
        if unique_match is not None:
            return cls(
                kind="paragraph",
                level=level,
                number=None,
                is_unique=True,
                text=unique_match.group("text").strip(),
                item=item,
                parent=parent,
            )
        match = PARAGRAPH_REGEX.match(text)
        assert match is not None
        return cls(
            kind="paragraph",
            level=level,
            number=match.group("number"),
            is_unique=False,
            text=match.group("text").strip(),
            item=item,
            parent=parent,
        )
