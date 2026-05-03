"""
models.py - Raw SQL schema and database connection for Tales of Time.

Replaces SQLAlchemy ORM entirely. Responsibilities:
  - Define the database connection factory
  - Define and create all 13 tables via raw DDL SQL
  - Provide a single get_db() function consumed by repositories
"""

import sqlite3
import os

# --- Connection ---

_HERE   = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.normpath(os.environ.get("DATABASE_PATH", os.path.join(_HERE, "..", "instance", "tales_of_time.db")))


def get_db() -> sqlite3.Connection:
    """
    Return a new SQLite connection with row_factory set so that
    all query results behave like dicts (row["ColumnName"]).

    Callers are responsible for closing the connection, or using
    it as a context manager (with get_db() as conn: ...).

    Foreign key enforcement is enabled on every connection -
    SQLite disables this by default.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# --- Schema DDL ---

# Each CREATE TABLE statement mirrors the specification exactly.
# IF NOT EXISTS means this is safe to call on every app start.

_SCHEMA = """

-- — Lookup / Reference tables ---

CREATE TABLE IF NOT EXISTS CharacterClass (
    ClassID     INTEGER PRIMARY KEY AUTOINCREMENT,
    ClassName   VARCHAR(50)  NOT NULL UNIQUE,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Species (
    SpeciesID   INTEGER PRIMARY KEY AUTOINCREMENT,
    SpeciesName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Alignment (
    AlignmentID   INTEGER PRIMARY KEY AUTOINCREMENT,
    AlignmentName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ItemType (
    ItemTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeName   VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Rarity (
    RarityID   INTEGER PRIMARY KEY AUTOINCREMENT,
    RarityName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Region (
    RegionID   INTEGER PRIMARY KEY AUTOINCREMENT,
    RegionName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Difficulty (
    DifficultyID   INTEGER PRIMARY KEY AUTOINCREMENT,
    DifficultyName VARCHAR(50) NOT NULL UNIQUE
);

-- — Core entities ---

CREATE TABLE IF NOT EXISTS Character (
    CharacterID   INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterName VARCHAR(100) NOT NULL,
    ClassID       INTEGER NOT NULL,
    SpeciesID     INTEGER NOT NULL,
    AlignmentID   INTEGER NOT NULL,
    Level         INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (ClassID)     REFERENCES CharacterClass(ClassID),
    FOREIGN KEY (SpeciesID)   REFERENCES Species(SpeciesID),
    FOREIGN KEY (AlignmentID) REFERENCES Alignment(AlignmentID)
);

CREATE TABLE IF NOT EXISTS Item (
    ItemID     INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName   VARCHAR(100) NOT NULL,
    ItemTypeID INTEGER NOT NULL,
    RarityID   INTEGER NOT NULL,
    FOREIGN KEY (ItemTypeID) REFERENCES ItemType(ItemTypeID),
    FOREIGN KEY (RarityID)   REFERENCES Rarity(RarityID)
);

CREATE TABLE IF NOT EXISTS Quest (
    QuestID      INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestName    VARCHAR(100) NOT NULL,
    RegionID     INTEGER NOT NULL,
    DifficultyID INTEGER NOT NULL,
    FOREIGN KEY (RegionID)     REFERENCES Region(RegionID),
    FOREIGN KEY (DifficultyID) REFERENCES Difficulty(DifficultyID)
);

-- — Join tables ---

CREATE TABLE IF NOT EXISTS Inventory (
    InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterID INTEGER NOT NULL,
    ItemID      INTEGER NOT NULL,
    Quantity    INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (CharacterID) REFERENCES Character(CharacterID),
    FOREIGN KEY (ItemID)      REFERENCES Item(ItemID)
);

CREATE TABLE IF NOT EXISTS CharacterQuest (
    CharacterQuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterID      INTEGER  NOT NULL,
    QuestID          INTEGER  NOT NULL,
    CompletionDate   DATETIME,
    FOREIGN KEY (CharacterID) REFERENCES Character(CharacterID),
    FOREIGN KEY (QuestID)     REFERENCES Quest(QuestID)
);

"""


def init_db() -> None:
    """
    Execute the schema DDL against the database.
    Safe to call on every startup - all statements use IF NOT EXISTS.
    Called by the Flask app factory instead of db.create_all().
    """
    with get_db() as conn:
        conn.executescript(_SCHEMA)
        conn.commit()