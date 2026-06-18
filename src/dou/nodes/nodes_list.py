from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dou.nodes.alinea_node import AlineaNode
    from dou.nodes.article_node import ArticleNode
    from dou.nodes.authority_node import AuthorityNode
    from dou.nodes.inciso_node import IncisoNode
    from dou.nodes.ministry_node import MinistryNode
    from dou.nodes.normative_act_node import NormativeActNode
    from dou.nodes.paragraph_node import ParagraphNode
    from dou.nodes.types import Node

CONTENT_NODE_KINDS = frozenset({"text", "list", "table"})


@dataclass
class NodesList:
    nodes: list[Node]

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def get_last_authority_node(self) -> AuthorityNode | None:
        for node in reversed(self.nodes):
            if node.kind == "authority":
                return node
        return None

    def get_last_ministry_node(self) -> MinistryNode | None:
        for node in reversed(self.nodes):
            if node.kind == "ministry":
                return node
        return None

    def get_last_normative_act_node(self) -> NormativeActNode | None:
        for node in reversed(self.nodes):
            if node.kind == "normative_act":
                return node
        return None

    def get_last_article_node(self) -> ArticleNode | None:
        for node in reversed(self.nodes):
            if node.kind == "article":
                return node
        return None

    def get_last_paragraph_node(self) -> ParagraphNode | None:
        for node in reversed(self.nodes):
            if node.kind == "paragraph":
                return node
        return None

    def get_last_inciso_node(self) -> IncisoNode | None:
        for node in reversed(self.nodes):
            if node.kind == "inciso":
                return node
        return None

    def get_last_alinea_node(self) -> AlineaNode | None:
        for node in reversed(self.nodes):
            if node.kind == "alinea":
                return node
        return None

    def get_inciso_parent(self) -> ArticleNode | ParagraphNode | None:
        for node in reversed(self.nodes):
            if node.kind in CONTENT_NODE_KINDS:
                continue
            if node.kind == "paragraph":
                return node
            if node.kind == "article":
                return node
        return None

    def get_current_parent(self) -> Node | None:
        for node in reversed(self.nodes):
            if node.kind in CONTENT_NODE_KINDS:
                continue
            return node
        return None
