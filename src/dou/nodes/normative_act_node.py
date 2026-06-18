from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, SectionHeaderItem

from dou.nodes.ministries import MINISTRIES
from dou.nodes.nodes_list import NodesList
from dou.nodes.section_header_node import SectionHeaderNode

ACT_TYPE = (
    r"INSTRU[ÇC][AÃ]O\s+NORMATIVA"
    r"|MEDIDA\s+PROVIS[ÓO]RIA"
    r"|DECRETO-LEI"
    r"|DECRETO"
    r"|RESOLU[ÇC][AÃ]O"
    r"|DELIBERA[ÇC][AÃ]O"
    r"|RETIFICA[ÇC][AÃ]O"
    r"|PORTARIA"
    r"|S[ÚU]MULA"
    r"|CIRCULAR"
    r"|LEI"
)

NORMATIVE_ACT_REGEX = re.compile(
    rf"^(?P<act_type>{ACT_TYPE})"
    r"(?:\s+(?P<abbreviation>.+?)(?=\s+N[ºo°]))?"
    r"\s+N[ºo°]\s*(?P<number>[\d.]+),?\s+"
    r"DE\s+(?P<day>\d{1,2})\s+DE\s+"
    r"(?P<month>JANEIRO|FEVEREIRO|MAR[ÇC]O|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)\s+"
    r"DE\s+(?P<year>\d{4})$",
    re.IGNORECASE,
)

MONTHS = {
    "JANEIRO": 1,
    "FEVEREIRO": 2,
    "MARCO": 3,
    "ABRIL": 4,
    "MAIO": 5,
    "JUNHO": 6,
    "JULHO": 7,
    "AGOSTO": 8,
    "SETEMBRO": 9,
    "OUTUBRO": 10,
    "NOVEMBRO": 11,
    "DEZEMBRO": 12,
}


@dataclass
class NormativeActNode:
    kind: Literal["normative_act"]
    level: int
    act_type: str
    abbreviation: str | None
    number: str
    date: datetime.date
    item: SectionHeaderNode

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, SectionHeaderItem):
            return False
        if item.text.strip() in MINISTRIES:
            return False
        parent = context.get_last_authority_node()
        if parent is None:
            return False
        return NORMATIVE_ACT_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(
        cls, item: SectionHeaderItem, level: int, context: NodesList
    ) -> NormativeActNode:
        header = SectionHeaderNode.from_item(item, level, context)
        match = NORMATIVE_ACT_REGEX.match(item.text.strip())
        assert match is not None
        month = MONTHS[match.group("month").upper().replace("Ç", "C")]
        return cls(
            kind="normative_act",
            level=level,
            act_type=match.group("act_type").upper(),
            abbreviation=match.group("abbreviation"),
            number=match.group("number").replace(".", ""),
            date=datetime.date(
                year=int(match.group("year")),
                month=month,
                day=int(match.group("day")),
            ),
            item=header,
        )

    @property
    def text(self) -> str:
        if self.abbreviation is None:
            return f"{self.act_type} {self.number} de {self.date}"
        return f"{self.act_type} {self.abbreviation} {self.number} de {self.date}"
