from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.nodes_list import NodesList
from dou.nodes.normative_act_node import NormativeActNode

ARTICLE_REGEX = re.compile(
    r"^Art\.\s+"
    r"(?P<number>\d+)"
    r"(?:-(?P<suffix>[A-Za-z]+))?"
    r"[º°oO]\s*"
    r"(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class ArticleNode:
    kind: Literal["article"]
    level: int
    number: str
    suffix: str | None
    text: str
    item: TextItem
    parent: NormativeActNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        if context.get_last_normative_act_node() is None:
            return False
        return ARTICLE_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> ArticleNode:
        parent = context.get_last_normative_act_node()
        assert parent is not None
        match = ARTICLE_REGEX.match(item.text.strip())
        assert match is not None
        return cls(
            kind="article",
            level=level,
            number=match.group("number"),
            suffix=match.group("suffix"),
            text=match.group("text").strip(),
            item=item,
            parent=parent,
        )
