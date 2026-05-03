"""
seed.py - This fills the tales of time database with lookup and sample transactional data.
----------------
Run after database creation: python database/seed.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import get_db, init_db

LOOKUP_SEED_DATA = {
    "CharacterClass": [
        {"ClassName": "Warrior", "Description": "A powerful melee fighter."},
        {"ClassName": "Mage", "Description": "A master of arcane magic."},
        {"ClassName": "Rogue", "Description": "A stealthy and cunning operative."},
        {"ClassName": "Paladin", "Description": "A holy warrior of righteousness."},
        {"ClassName": "Ranger", "Description": "A skilled hunter of the wilds."},
        {"ClassName": "Necromancer",  "Description": "A master of death magic."},
    ],
    "Species": [
        {"SpeciesName": "Human"},
        {"SpeciesName": "Dwarf"},
        {"SpeciesName": "Elf"},
        {"SpeciesName": "Orc"},
        {"SpeciesName": "Halfling"},
    ],
    "Alignment": [
        {"AlignmentName": "Lawful Good"},
        {"AlignmentName": "Neutral Good"},
        {"AlignmentName": "Chaotic Good"},
        {"AlignmentName": "Lawful Neutral"},
        {"AlignmentName": "True Neutral"},
        {"AlignmentName": "Chaotic Neutral"},
        {"AlignmentName": "Lawful Evil"},
        {"AlignmentName": "Neutral Evil"},
        {"AlignmentName": "Chaotic Evil"},
    ],
    "ItemType": [
        {"TypeName": "Weapon"},
        {"TypeName": "Armour"},
        {"TypeName": "Potion"},
        {"TypeName": "Accessory"},
        {"TypeName": "Quest Item"},
    ],
    "Rarity": [
        {"RarityName": "Common"},
        {"RarityName": "Uncommon"},
        {"RarityName": "Rare"},
        {"RarityName": "Epic"},
        {"RarityName": "Legendary"},
    ],
    "Region": [
        {"RegionName": "The Verdant Vale"},
        {"RegionName": "Shadowfen Marshes"},
        {"RegionName": "Ironpeak Mountains"},
        {"RegionName": "The Ashen Wastes"},
        {"RegionName": "Crystalspire Forest"},
    ],
    "Difficulty": [
        {"DifficultyName": "Novice"},
        {"DifficultyName": "Journeyman"},
        {"DifficultyName": "Adept"},
        {"DifficultyName": "Expert"},
        {"DifficultyName": "Legendary"},
    ],
}


def seed_lookup_tables(conn):
    for table, rows in LOOKUP_SEED_DATA.items():
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count == 0:
            for row in rows:
                cols = ", ".join(row.keys())
                placeholders = ", ".join(["?"] * len(row))
                conn.execute(
                    f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
                    list(row.values())
                )
            print(f" Seeded {table}")
        else:
            print(f" Skipped {table} (already has data)")
    conn.commit()


def seed_core_data(conn):
    # - Lookup helpers -
    classes      = {r["ClassName"]:      r["ClassID"]      for r in conn.execute("SELECT ClassID, ClassName FROM CharacterClass").fetchall()}
    species      = {r["SpeciesName"]:    r["SpeciesID"]    for r in conn.execute("SELECT SpeciesID, SpeciesName FROM Species").fetchall()}
    alignments   = {r["AlignmentName"]:  r["AlignmentID"]  for r in conn.execute("SELECT AlignmentID, AlignmentName FROM Alignment").fetchall()}
    item_types   = {r["TypeName"]:       r["ItemTypeID"]   for r in conn.execute("SELECT ItemTypeID, TypeName FROM ItemType").fetchall()}
    rarities     = {r["RarityName"]:     r["RarityID"]     for r in conn.execute("SELECT RarityID, RarityName FROM Rarity").fetchall()}
    regions      = {r["RegionName"]:     r["RegionID"]     for r in conn.execute("SELECT RegionID, RegionName FROM Region").fetchall()}
    difficulties = {r["DifficultyName"]: r["DifficultyID"] for r in conn.execute("SELECT DifficultyID, DifficultyName FROM Difficulty").fetchall()}

    # - Characters -
    if conn.execute("SELECT COUNT(*) FROM Character").fetchone()[0] == 0:
        character_rows = [
            ("Thorin Ironblade", classes["Warrior"], species["Dwarf"],    alignments["Lawful Good"],    12),
            ("Aelindra Swift",   classes["Ranger"],  species["Elf"],      alignments["Chaotic Good"],    7),
            ("Grommash",         classes["Warrior"], species["Orc"],      alignments["Chaotic Neutral"], 5),
            ("Seraphina Vale",   classes["Paladin"], species["Human"],    alignments["Lawful Good"],     9),
            ("Zyx Shadowmeld",   classes["Rogue"],   species["Halfling"], alignments["True Neutral"],    3),
        ]
        conn.executemany(
            "INSERT INTO Character (CharacterName, ClassID, SpeciesID, AlignmentID, Level) VALUES (?, ?, ?, ?, ?)",
            character_rows
        )
        conn.commit()
        print(" Seeded Character")
    else:
        print(" Skipped Character (already has data)")

    char_map = {r["CharacterName"]: r["CharacterID"] for r in conn.execute("SELECT CharacterID, CharacterName FROM Character").fetchall()}

    # - Items -
    if conn.execute("SELECT COUNT(*) FROM Item").fetchone()[0] == 0:
        item_rows = [
            ("Iron Sword",        item_types["Weapon"],    rarities["Common"]),
            ("Leather Armour",    item_types["Armour"],    rarities["Common"]),
            ("Healing Potion",    item_types["Potion"],    rarities["Uncommon"]),
            ("Elven Longbow",     item_types["Weapon"],    rarities["Rare"]),
            ("Ring of Swiftness", item_types["Accessory"], rarities["Epic"]),
            ("Shadowblade",       item_types["Weapon"],    rarities["Legendary"]),
        ]
        conn.executemany(
            "INSERT INTO Item (ItemName, ItemTypeID, RarityID) VALUES (?, ?, ?)",
            item_rows
        )
        conn.commit()
        print(" seeded Item")
    else:
        print(" Skipped Item (already has data)")

    item_map = {r["ItemName"]: r["ItemID"] for r in conn.execute("SELECT ItemID, ItemName FROM Item").fetchall()}

    # - Quests -
    if conn.execute("SELECT COUNT(*) FROM Quest").fetchone()[0] == 0:
        quest_rows = [
            ("Defend the Vale",       regions["The Verdant Vale"],    difficulties["Journeyman"]),
            ("The Marsh Wraith",      regions["Shadowfen Marshes"],   difficulties["Adept"]),
            ("Summit of Ironpeak",    regions["Ironpeak Mountains"],  difficulties["Expert"]),
            ("Embers of the Wastes",  regions["The Ashen Wastes"],    difficulties["Novice"]),
            ("The Crystal Labyrinth", regions["Crystalspire Forest"], difficulties["Legendary"]),
        ]
        conn.executemany(
            "INSERT INTO Quest (QuestName, RegionID, DifficultyID) VALUES (?, ?, ?)",
            quest_rows
        )
        conn.commit()
        print(" Seeded Quest")
    else:
        print(" Skipped Quest (already has data)")

    quest_map = {r["QuestName"]: r["QuestID"] for r in conn.execute("SELECT QuestID, QuestName FROM Quest").fetchall()}

    # -— Inventory -
    if conn.execute("SELECT COUNT(*) FROM Inventory").fetchone()[0] == 0:
        inventory_rows = [
            (char_map["Thorin Ironblade"], item_map["Iron Sword"],        1),
            (char_map["Thorin Ironblade"], item_map["Healing Potion"],    3),
            (char_map["Aelindra Swift"], item_map["Elven Longbow"],     1),
            (char_map["Aelindra Swift"], item_map["Ring of Swiftness"], 1),
            (char_map["Grommash"],  item_map["Leather Armour"],    1),
            (char_map["Zyx Shadowmeld"], item_map["Shadowblade"],       1),
        ]
        conn.executemany(
            "INSERT INTO Inventory (CharacterID, ItemID, Quantity) VALUES (?, ?, ?)",
            inventory_rows
        )
        conn.commit()
        print("  Seeded Inventory")
    else:
        print(" Skipped Inventory (already has data)")

    # - CharacterQuest -
    if conn.execute("SELECT COUNT(*) FROM CharacterQuest").fetchone()[0] == 0:
        cq_rows = [
            (char_map["Thorin Ironblade"], quest_map["Defend the Vale"], datetime(2026, 1, 12, 14, 30)),
            (char_map["Aelindra Swift"], quest_map["The Marsh Wraith"],  datetime(2026, 2,  3, 10,  0)),
            (char_map["Seraphina Vale"], quest_map["Summit of Ironpeak"], None),
            (char_map["Grommash"], quest_map["Embers of the Wastes"], datetime(2026, 3,  7,  9, 15)),
            (char_map["Zyx Shadowmeld"], quest_map["The Crystal Labyrinth"], None),
        ]
        conn.executemany(
            "INSERT INTO CharacterQuest (CharacterID, QuestID, CompletionDate) VALUES (?, ?, ?)",
            cq_rows
        )
        conn.commit()
        print(" Seeded CharacterQuest")
    else:
        print(" Skipped CharacterQuest (already has data)")


def seed():
    init_db()
    with get_db() as conn:
        seed_lookup_tables(conn)
        seed_core_data(conn)
    print("\nSeed complete.")


if __name__ == "__main__":
    seed()