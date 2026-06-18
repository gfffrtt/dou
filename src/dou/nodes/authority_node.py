from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, SectionHeaderItem

from dou.nodes.ministries import MINISTRIES
from dou.nodes.ministry_node import MinistryNode
from dou.nodes.nodes_list import NodesList
from dou.nodes.section_header_node import SectionHeaderNode


@dataclass
class AuthorityNode:
    kind: Literal["authority"]
    level: int
    text: str
    item: SectionHeaderNode
    parent: MinistryNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, SectionHeaderItem):
            return False
        if item.text.strip() in MINISTRIES:
            return False
        from dou.nodes.normative_act_node import NormativeActNode

        if NormativeActNode.matches(item, level, context):
            return False
        return context.get_last_ministry_node() is not None

    @classmethod
    def from_item(
        cls, item: SectionHeaderItem, level: int, context: NodesList
    ) -> AuthorityNode:
        header = SectionHeaderNode.from_item(item, level, context)
        parent = context.get_last_ministry_node()
        assert parent is not None
        return cls(
            text=item.text,
            level=level,
            item=header,
            kind="authority",
            parent=parent,
        )
