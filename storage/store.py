import sqlite3
import os
import json
import hashlib
from core.memory import MemoryEntry

DB_PATH = "memory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS memory_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        score REAL DEFAULT 0.0,
        created_at REAL,
        updated_at REAL,
        usage_count INTEGER DEFAULT 0,
        tags TEXT,
        version INTEGER DEFAULT 1,
        text_hash TEXT
    );
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS memory_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT,
        created_at REAL
    );
    ''')

    conn.commit()
    conn.close()

def normalize_text(text):
    return ' '.join(text.strip().lower().split())

def hash_text(text):
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def save_memory(entries):
    conn = get_connection()
    cursor = conn.cursor()

    for e in entries:
        text_hash = hash_text(e.text)
        cursor.execute('SELECT id FROM memory_entries WHERE text_hash = ?', (text_hash,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"Skipping existing entry: {e.text[:30]}...")
            continue

        tags_json = json.dumps(e.tags)

        cursor.execute(''' 
        INSERT INTO memory_entries (text, score, created_at, updated_at, usage_count, tags, text_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (e.text, e.score, e.created_at, e.created_at, e.usage_count, tags_json, text_hash))

    conn.commit()
    conn.close()

def load_memory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT text, score, created_at, usage_count, tags FROM memory_entries')
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        tags = json.loads(row[4])
        score = float(row[1])
        e = MemoryEntry(
            text=row[0],
            score=score,
            created_at=row[2],
            usage_count=row[3],
            tags=tags
        )
        entries.append(e)

    return entries

def backfill_text_hashes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, text FROM memory_entries WHERE text_hash IS NULL')
    rows = cursor.fetchall()

    for row in rows:
        entry_id, text = row
        h = hash_text(text)
        cursor.execute('UPDATE memory_entries SET text_hash = ? WHERE id = ?', (h, entry_id))

    conn.commit()
    conn.close()
