from pathlib import Path

from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import (
    ListItem,
    SectionHeaderItem,
    TableItem,
    TextItem,
)

from dou.nodes.alinea_node import AlineaNode
from dou.nodes.article_node import ArticleNode
from dou.nodes.authority_node import AuthorityNode
from dou.nodes.inciso_node import IncisoNode
from dou.nodes.item_node import ItemNode
from dou.nodes.list_node import ListNode
from dou.nodes.ministry_node import MinistryNode
from dou.nodes.nodes_list import NodesList
from dou.nodes.normative_act_node import NormativeActNode
from dou.nodes.paragraph_node import ParagraphNode
from dou.nodes.section_header_node import SectionHeaderNode
from dou.nodes.table_node import TableNode
from dou.nodes.text_node import TextNode

SECTION_HEADER_RESOLVERS = [
    MinistryNode,
    NormativeActNode,
    AuthorityNode,
    SectionHeaderNode,
]

TEXT_ITEM_RESOLVERS = [
    ArticleNode,
    ParagraphNode,
    IncisoNode,
    AlineaNode,
    ItemNode,
    TextNode,
]

ITEM_RESOLVERS: list[tuple[type, list[type]]] = [
    (SectionHeaderItem, SECTION_HEADER_RESOLVERS),
    (TextItem, TEXT_ITEM_RESOLVERS),
    (TableItem, [TableNode]),
    (ListItem, [ListNode]),
]


async def nodes(
    pdf_path: str | Path,
) -> NodesList:
    converter = DocumentConverter()
    doc = converter.convert(pdf_path).document
    nodes_list = NodesList(nodes=[])
    for item, level in doc.iterate_items():
        for item_type, resolvers in ITEM_RESOLVERS:
            if isinstance(item, item_type):
                for resolver in resolvers:
                    if resolver.matches(item, level, nodes_list):
                        nodes_list.add_node(resolver.from_item(item, level, nodes_list))
                        break
                break
    return nodes_list
