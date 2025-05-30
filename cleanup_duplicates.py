import sqlite3
import hashlib

DB_PATH = "memory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def cleanup_duplicates():
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Fetch all entries with their text + id
    cursor.execute("SELECT id, text FROM memory_entries")
    entries = cursor.fetchall()

    seen_hashes = set()
    to_delete = []

    for entry_id, text in entries:
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if text_hash in seen_hashes:
            to_delete.append(entry_id)
        else:
            seen_hashes.add(text_hash)

    # Step 2: Delete duplicates
    if to_delete:
        cursor.executemany("DELETE FROM memory_entries WHERE id = ?", [(i,) for i in to_delete])
        print(f"🧹 Deleted {len(to_delete)} duplicate entries.")
    else:
        print("✅ No duplicates found.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    cleanup_duplicates()
