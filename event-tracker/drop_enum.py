import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# # Strip +asyncpg for asyncpg connect()
# if "+asyncpg" in DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

DATABASE_URL = "postgresql://postgres:Shraya%4017@localhost:5432/event_tracker"

async def drop_enum_type():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('DROP TYPE IF EXISTS roleenum CASCADE;')
        print("Dropped enum type 'roleenum' if it existed.")
    except Exception as e:
        print(f"Error dropping enum: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(drop_enum_type())
