import asyncio
from databases import Database
import os

DBHOST = os.getenv("POSTGRES_HOST", "localhost")
DBUSER = os.getenv("DBUSER", "postgres")
DBPOOL_MIN = os.getenv("DBPOOL_MIN", "2")
DBPOOL_MAX = os.getenv("DBPOOL_MAX", "8")
database = Database(
    f"postgresql://{DBUSER}@{DBHOST}/test?min_size={DBPOOL_MIN}&max_size={DBPOOL_MAX}"
)


async def main():
    await database.connect()

    query = """CREATE TABLE IF NOT EXISTS mytbl (
        id SERIAL, key VARCHAR(32)
    )
    """
    await database.execute(query=query)

    query = "INSERT INTO mytbl(key) VALUES (:key)"
    values = ["fi", "fo", "fum"]
    await database.execute_many(query=query, values=[{"key": val} for val in values])

    query = "SELECT key FROM mytbl"
    rows = await database.fetch_all(query=query)
    print("DB now contains {} rows".format(len(rows)))

asyncio.run(main())
