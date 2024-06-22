from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO telegram_users (full_name, username, telegram_id, created_at, updated_at) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, datetime.now(), datetime.now(), fetchrow=True)

    async def add_food(self, user_id: int, name: str):
        sql = "SELECT * FROM foods WHERE name=$1"
        result = await self.execute(sql, name, fetchrow=True)
        if not result:
            await self.execute(
                "INSERT INTO foods (name, created_at, updated_at) VALUES ($1, $2, $3)",
                name, datetime.now(), datetime.now(), fetchrow=True
            )
        sql = "INSERT INTO user_foods (user_id, name, created_at, updated_at) VALUES ($1, $2, $3, $4) RETURNING *"
        return await self.execute(sql, user_id, name, datetime.now(), datetime.now(), fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM telegram_users"
        return await self.execute(sql, fetch=True)

    async def select_all_foods(self):
        sql = "SELECT * FROM foods"
        return await self.execute(sql, fetch=True)

    async def select_user_foods(self, user_id: int):
        sql = "SELECT * FROM user_foods"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM telegram_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM telegram_users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE telegram_users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM telegram_users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE telegram_users", execute=True)
