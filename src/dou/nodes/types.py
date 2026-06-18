from __future__ import annotations

from dou.nodes.alinea_node import AlineaNode
from dou.nodes.article_node import ArticleNode
from dou.nodes.authority_node import AuthorityNode
from dou.nodes.inciso_node import IncisoNode
from dou.nodes.item_node import ItemNode
from dou.nodes.list_node import ListNode
from dou.nodes.ministry_node import MinistryNode
from dou.nodes.normative_act_node import NormativeActNode
from dou.nodes.paragraph_node import ParagraphNode
from dou.nodes.section_header_node import SectionHeaderNode
from dou.nodes.table_node import TableNode
from dou.nodes.text_node import TextNode

type Node = (
    TextNode
    | ArticleNode
    | ParagraphNode
    | IncisoNode
    | AlineaNode
    | ItemNode
    | TableNode
    | SectionHeaderNode
    | ListNode
    | MinistryNode
    | AuthorityNode
    | NormativeActNode
)
