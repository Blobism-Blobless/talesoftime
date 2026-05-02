-- schema.sql - Tales of Time database schema
-- Run once to create all tables: python database/init_db.py

PRAGMA foreign_keys = ON;

-- ── Lookup tables ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS CharacterClass (
    ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClassName VARCHAR(50) NOT NULL UNIQUE,
    Description TEXT
)

CREATE TABLE IF NOT EXISTS Species (
    SpeciesID INTEGER PRIMARY KEY AUTOINCREMENT,
    SpeciesName VARCHAR(50) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS Alignment (
    AlignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    AlignmentName VARCHAR(50) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS ItemType (
    ItemTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemTypeName VARCHAR(50) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS Rarity (
    RarityID INTEGER PRIMARY KEY AUTOINCREMENT,
    RarityName VARCHAR(50) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS Region (
    RegionID INTEGER PRIMARY KEY AUTOINCREMENT,
    RegionName VARCHAR(100) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS Difficulty (
    DifficultyID INTEGER PRIMARY KEY AUTOINCREMENT,
    DifficultyName VARCHAR(50) NOT NULL UNIQUE,
)
-- ── Core entities ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS Character (
    CharacterID INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterName VARCHAR(100) NOT NULL UNIQUE,
    ClassID INTEGER NOT NULL REFERENCES CharacterClass(ClassID),
    SpeciesID INTEGER NOT NULL REFERENCES Species(SpeciesID),
    AlignmentID INTEGER NOT NULL REFERENCES Alignment(AlignmentID),
    Level INTEGER NOT NULL DEFAULT 1
)

CREATE TABLE IF NOT EXISTS Item (
    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName VARCHAR(100) NOT NULL UNIQUE,
    ItemTypeID INTEGER NOT NULL REFERENCES ItemType(ItemTypeID),
    RarityID INTEGER NOT NULL REFERENCES Rarity(RarityID),
)

CREATE TABLE IF NOT EXISTS Quest (
    QuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestName VARCHAR(100) NOT NULL UNIQUE,
    RegionID INTEGER NOT NULL REFERENCES Region(RegionID),
    DifficultyID INTEGER NOT NULL REFERENCES Difficulty(DifficultyID),
)

-- ── Join tables ───────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS Inventory (
    InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterID INTEGER NOT NULL REFERENCES Character(CharacterID) ON DELETE CASCADE,
    ItemID INTEGER NOT NULL REFERENCES Item(ItemID),
    Quantity INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS CharacterQuest (
    CharacterQuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    CharacterID INTEGER NOT NULL REFERENCES Character(CharacterID) ON DELETE CASCADE,
    QuestID INTEGER NOT NULL REFERENCES Quest(QuestID),
    CompletionDate DATETIME NULL
);