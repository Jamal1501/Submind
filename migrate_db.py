import sqlite3

DB_PATH = "memory.db"

def add_text_hash_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE memory_entries ADD COLUMN text_hash TEXT;")
        print("✅ Column 'text_hash' added.")
    except sqlite3.OperationalError as e:
        print("⚠️ Already has 'text_hash' column or another issue:", e)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_text_hash_column()
