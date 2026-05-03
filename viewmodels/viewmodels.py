"""
viewmodels.py - ViewModel layer for Tales of Time.

Transforms sqlite3.Row objects (dict-like) into plain dataclasses
that templates consume. Access pattern changes from ORM attribute
access (row.ColumnName) to key access (row["ColumnName"]).
"""

from dataclasses import dataclass, field
from typing import List, Optional


# --- Character ---

@dataclass
class CharacterViewModel:
    character_id:    int
    name:            str
    level:           int
    character_class: str
    species:         str
    alignment:       str

    @classmethod
    def from_row(cls, row) -> "CharacterViewModel":
        return cls(
            character_id    = row["CharacterID"],
            name            = row["CharacterName"],
            level           = row["Level"],
            character_class = row["ClassName"],
            species         = row["SpeciesName"],
            alignment       = row["AlignmentName"],
        )


@dataclass
class CharacterListViewModel:
    characters: List[CharacterViewModel] = field(default_factory=list)
    total:      int = 0

    @classmethod
    def from_rows(cls, rows) -> "CharacterListViewModel":
        vms = [CharacterViewModel.from_row(r) for r in rows]
        return cls(characters=vms, total=len(vms))


@dataclass
class CharacterFormViewModel:
    """Carries dropdown options for the create / edit form."""
    classes:    list = field(default_factory=list)
    species:    list = field(default_factory=list)
    alignments: list = field(default_factory=list)
    character:  Optional[object] = None   # None = create mode, Row = edit mode


# --- Item ---

@dataclass
class ItemViewModel:
    item_id:   int
    name:      str
    item_type: str
    rarity:    str

    @classmethod
    def from_row(cls, row) -> "ItemViewModel":
        return cls(
            item_id   = row["ItemID"],
            name      = row["ItemName"],
            item_type = row["TypeName"],
            rarity    = row["RarityName"],
        )


@dataclass
class ItemListViewModel:
    items: List[ItemViewModel] = field(default_factory=list)
    total: int = 0

    @classmethod
    def from_rows(cls, rows) -> "ItemListViewModel":
        vms = [ItemViewModel.from_row(r) for r in rows]
        return cls(items=vms, total=len(vms))


@dataclass
class ItemFormViewModel:
    item_types: list = field(default_factory=list)
    rarities:   list = field(default_factory=list)


# --- Quest ---

@dataclass
class QuestViewModel:
    quest_id:   int
    name:       str
    region:     str
    difficulty: str

    @classmethod
    def from_row(cls, row) -> "QuestViewModel":
        return cls(
            quest_id   = row["QuestID"],
            name       = row["QuestName"],
            region     = row["RegionName"],
            difficulty = row["DifficultyName"],
        )


@dataclass
class QuestListViewModel:
    quests: List[QuestViewModel] = field(default_factory=list)
    total:  int = 0

    @classmethod
    def from_rows(cls, rows) -> "QuestListViewModel":
        vms = [QuestViewModel.from_row(r) for r in rows]
        return cls(quests=vms, total=len(vms))


@dataclass
class QuestFormViewModel:
    regions:      list = field(default_factory=list)
    difficulties: list = field(default_factory=list)


# --- Inventory ---

@dataclass
class InventoryEntryViewModel:
    inventory_id: int
    item_name:    str
    item_type:    str
    rarity:       str
    quantity:     int

    @classmethod
    def from_row(cls, row) -> "InventoryEntryViewModel":
        return cls(
            inventory_id = row["InventoryID"],
            item_name    = row["ItemName"],
            item_type    = row["TypeName"],
            rarity       = row["RarityName"],
            quantity     = row["Quantity"],
        )


# --- CharacterQuest ---

@dataclass
class CharacterQuestViewModel:
    cq_id:           int
    quest_name:      str
    region:          str
    difficulty:      str
    completion_date: Optional[str]

    @property
    def is_complete(self) -> bool:
        return self.completion_date is not None

    @classmethod
    def from_row(cls, row) -> "CharacterQuestViewModel":
        return cls(
            cq_id           = row["CharacterQuestID"],
            quest_name      = row["QuestName"],
            region          = row["RegionName"],
            difficulty      = row["DifficultyName"],
            completion_date = row["CompletionDate"],
        )


# --- Dashboard ---

@dataclass
class DashboardViewModel:
    total_characters: int = 0
    total_items:      int = 0
    total_quests:     int = 0
