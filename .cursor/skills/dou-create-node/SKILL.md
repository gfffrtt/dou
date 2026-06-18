---
name: dou-create-node
description: >-
  Create new Docling item resolvers (nodes) in the dou PDF pipeline.
  Use when adding a node type, extending nodes.py resolvers, or implementing
  matches/from_item for ministry, authority, normative_act, article, text, etc.
---

# Criar nodes no dou

## Arquitetura

O pipeline em `src/dou/nodes/nodes.py` converte um PDF com Docling e percorre `doc.iterate_items()`. Para cada item, tenta resolvers na ordem definida em `ITEM_RESOLVERS` até `matches()` retornar `True`.

```
PDF → DocumentConverter → iterate_items() → resolver.matches() → resolver.from_item() → NodesList
```

Cada node é um `@dataclass` em `src/dou/nodes/<nome>_node.py`, registrado em `types.py` e em `nodes.py`.

## Checklist

1. Criar `src/dou/nodes/<nome>_node.py`
2. Adicionar o tipo ao union `Node` em `types.py`
3. Registrar no resolver correto em `nodes.py` (ordem importa — mais específico primeiro)
4. Se precisar de contexto novo, estender `NodesList` em `nodes_list.py`

## Template de node

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from docling_core.types.doc.document import DocItem, TextItem

from dou.nodes.nodes_list import NodesList

MEU_REGEX = re.compile(r"^...$", re.IGNORECASE)


@dataclass
class MeuNode:
    kind: Literal["meu_kind"]
    level: int
    text: str
    item: TextItem

    @classmethod
    def matches(cls, item: DocItem, level: int, context: NodesList) -> bool:
        if not isinstance(item, TextItem):
            return False
        parent = context.get_current_parent()
        if parent is None or parent.kind != "normative_act":
            return False
        return MEU_REGEX.match(item.text.strip()) is not None

    @classmethod
    def from_item(cls, item: TextItem, level: int, context: NodesList) -> MeuNode:
        match = MEU_REGEX.match(item.text.strip())
        assert match is not None
        return cls(
            kind="meu_kind",
            level=level,
            text=match.group("text").strip(),
            item=item,
        )
```

## Convenções

### Estrutura da classe

- `@dataclass` com campo `kind: Literal["..."]` discriminando o tipo
- `level: int` sempre presente
- `item` guarda o `DocItem` original do Docling
- `parent` quando o node pertence a outro node estrutural (ex.: `NormativeActNode`, `MinistryNode`)
- Dois classmethods obrigatórios: `matches()` e `from_item()`

### Regex

- Constantes de módulo em UPPER_SNAKE_CASE (`ARTICLE_REGEX`, `NORMATIVE_ACT_REGEX`)
- Usar `re.compile` com named groups
- Em `matches()`, usar `.match(text.strip())` no início da string
- Em `from_item()`, `assert match is not None` após `matches()` ter passado

### Proibido

- Métodos com prefixo `_` em classes de node
- Helpers privados na classe — regex e lógica ficam no módulo ou inline em `matches()` / `from_item()`

### Resolvers em `nodes.py`

```python
SECTION_HEADER_RESOLVERS = [
    MinistryNode,       # mais específico
    NormativeActNode,
    AuthorityNode,
    SectionHeaderNode,  # fallback genérico
]

TEXT_ITEM_RESOLVERS = [
    ArticleNode,  # mais específico
    TextNode,     # fallback genérico
]

ITEM_RESOLVERS: list[tuple[type, list[type]]] = [
    (SectionHeaderItem, SECTION_HEADER_RESOLVERS),
    (TextItem, TEXT_ITEM_RESOLVERS),
    (TableItem, [TableNode]),
    (ListItem, [ListNode]),
]
```

O primeiro resolver que der `matches() == True` vence. Coloque variantes específicas antes do fallback genérico.

## Contexto em `NodesList`

| Método | Uso |
|--------|-----|
| `get_current_parent()` | Parent estrutural mais recente: percorre de trás pra frente ignorando `text`, `article`, `list`, `table` |
| `get_last_ministry_node()` | Último ministry na lista (para `AuthorityNode.parent`) |
| `get_last_authority_node()` | Último authority na lista (para `NormativeActNode`) |

### Quando usar cada parent

- **Conteúdo** (`ArticleNode`, futuros parágrafos/incisos): `get_current_parent()` — exige que o parent estrutural mais recente seja do tipo esperado (ex.: `normative_act`).
- **Ato normativo**: `get_last_authority_node()` — deve existir um authority na hierarquia.
- **Authority**: `get_last_ministry_node()` — deve existir um ministry na hierarquia.

`get_current_parent()` garante que um `TextItem` logo após um `ministry` **não** vira artigo, mesmo que exista um `normative_act` mais antigo na lista.

## Referências existentes

| Node | DocItem | Parent / contexto |
|------|---------|-------------------|
| `MinistryNode` | `SectionHeaderItem` | texto em `MINISTRIES` |
| `AuthorityNode` | `SectionHeaderItem` | `get_last_ministry_node()`; não é normative act |
| `NormativeActNode` | `SectionHeaderItem` | `get_last_authority_node()` |
| `ArticleNode` | `TextItem` | `get_current_parent().kind == "normative_act"`; regex `Art. N[º°oO]` |
| `TextNode` | `TextItem` | fallback — sempre casa |
| `SectionHeaderNode` | `SectionHeaderItem` | fallback de cabeçalho |

## Exemplo: ArticleNode

Regex com sufixo opcional (`Art. 1º-A`):

```python
ARTICLE_REGEX = re.compile(
    r"^Art\.\s+"
    r"(?P<number>\d+)"
    r"(?:-(?P<suffix>[A-Za-z]+))?"
    r"[º°oO]\s*"
    r"(?P<text>.*)$",
    re.IGNORECASE | re.DOTALL,
)
```

Campos extraídos: `number` (só dígitos), `suffix` (`None` ou `"A"`), `text` (corpo após identificador).
