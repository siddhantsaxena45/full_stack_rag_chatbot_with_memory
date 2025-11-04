import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("❌ DATABASE_URL not found in .env")

try:
    print("Connecting to database...")
    conn = psycopg2.connect(DB_URL, sslmode="require")  # 👈 Add this line
    print("✅ Database connection successful")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            prompt TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    cur.close()
    print("✅ Tables created successfully")

except Exception as error:
    print(f"❌ Database error: {error}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("🔒 Connection closed")
