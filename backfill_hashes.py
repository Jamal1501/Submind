import sqlite3
import hashlib

DB_PATH = "memory.db"

def backfill_text_hashes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM memory_entries WHERE text_hash IS NULL OR text_hash = ''")
    rows = cursor.fetchall()

    updated = 0
    for row in rows:
        entry_id, text = row
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        cursor.execute("UPDATE memory_entries SET text_hash = ? WHERE id = ?", (text_hash, entry_id))
        updated += 1

    conn.commit()
    conn.close()
    print(f"✅ Backfilled {updated} entries.")

if __name__ == "__main__":
    backfill_text_hashes()
