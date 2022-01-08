from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        total BIGINT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        file_name VARCHAR(255) NULL,
        path_url_send_file VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, total, telegram_id,file_name,path_url_send_file):
        sql = "INSERT INTO users (full_name, total, telegram_id,file_name,path_url_send_file) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, total, telegram_id, file_name, path_url_send_file, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_tottal_price(self, total, telegram_id):
        sql = "UPDATE Users SET total=$1 WHERE telegram_id=$2"
        return await self.execute(sql, total, telegram_id, execute=True)

    async def update_path_url_send_file(self, path_url_send_file, telegram_id):
        sql = "UPDATE Users SET path_url_send_file=$1 WHERE telegram_id=$2"
        return await self.execute(sql, path_url_send_file, telegram_id, execute=True)

    async def update_file_name(self, file_name, telegram_id):
        sql = "UPDATE Users SET file_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, file_name, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)