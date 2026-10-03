import asyncpg

from config import db_settings

### two users from different source channel, filling address .

class Connection:
     _pool = None

     @classmethod
     async def creating_pool(cls):
          cls._pool =  await asyncpg.create_pool(host=db_settings.db_host, port=db_settings.db_port, user=db_settings.db_user, database=db_settings.db_database,
                                                  password=db_settings.postgres_password, min_size=db_settings.db_min_connection_pool, max_size=db_settings.db_max_connection_pool)

     @classmethod
     async def fetch_all(cls, query, *args):
          if cls._pool is None:
               raise RuntimeError("Database pool is not initialized")

          async with cls._pool.acquire() as conn:
               async with conn.transaction():
                    cursor = await conn.cursor(query, *args)
                    records = []
                    while data := await cursor.fetch(5):
                         records.extend(data)
                    return records

     @classmethod
     async def fetch_one(cls, query, *args):
          if cls._pool is None:
               raise RuntimeError("Database pool is not initialized")

          async with cls._pool.acquire() as conn:
               return await conn.fetchrow(query, *args)

     @classmethod
     async def execute_query(cls, query, *args):
          if cls._pool is None:
               raise RuntimeError("Database pool is not initialized")

          async with cls._pool.acquire() as conn:
               # if "RETURNING" in query:
               #      return await conn.fetchrow(query, *args)
               return await conn.execute(query, *args)

     @classmethod
     async def execute_batch_query(cls, query, *args):
          if cls._pool is None:
               raise RuntimeError("Database pool is not initialized")

          async with cls._pool.acquire() as conn:
               # if "RETURNING" in query:
               #      return await conn.fetchrow(query, *args)
               return await conn.executemany(query, *args)

     @classmethod
     async def create_transactional_connection(cls, foo):
          async with cls._pool.acquire() as conn:
               async with conn.transaction():
                    await foo()











#     async def connect_to_postgres(self):
#          async with asyncpg.create_pool(host='localhost', port=5432, user='postgres', database='mcidb', password='1234', min_size=6, max_size=6) as pool:
#               return pool
