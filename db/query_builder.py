from pydantic import BaseModel
import asyncio

from db.connection import Connection
from typing import List



class QueryBuilder:
    def __init__(self, table_name):
        self.table_name = table_name


    async def insert_row(self, base_model: BaseModel, returning_column: str | None = None):
        query = "INSERT INTO {table} ({columns}) VALUES ({values}) {return_column};".\
        format(table=self.table_name,
               columns = ",".join(list(base_model.model_dump().keys())),
               values = ",".join([f"(${n + 1})" for n in range(len(base_model.model_dump().values()))]),
               return_column = ("RETURNING " + returning_column) if returning_column else "")
        print(query)
        if returning_column:
            return await Connection.fetch_one(query, *base_model.model_dump().values())

        return await Connection.execute_query(query, *base_model.model_dump().values())


    async def insert_many_row(self, base_model: type[BaseModel], data_models: list[BaseModel]):
        query = "INSERT INTO {table} ({columns}) VALUES ({values});".\
        format(table=self.table_name,
               columns = ",".join(list(base_model.model_fields.keys())),
               values = ",".join([f"(${n + 1})" for n in range(len(base_model.model_fields.keys()))]),
        )
        print(query)
        # breakpoint()
        return await Connection.execute_batch_query(query, [tuple(data_model.model_dump().values()) for data_model in data_models])
    

    async def select(self, column: List='*', condition: str=None, group: list=None, order: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None, condition_constant: list=[]):
        query = "SELECT {columns} FROM {table} {condition} {group} {order} {asc_or_desc} {limit} {offset}".\
        format(columns=",".join(list(column)) if type(column) == list else "*",
               table=self.table_name,
               condition=("WHERE " + condition) if condition else "",
                group="GROUP BY " + ",".join(group) if group else "",
                order="ORDER BY " + order if order else "",
                asc_or_desc=asc_or_desc if asc_or_desc else "",
                limit="LIMIT " + str(limit) if limit else "",
                offset="OFFSET " + str(offset) if offset else "")
        return await Connection.fetch_all(query, *condition_constant)


    ### returns a record that automatically converts into json by fastapi upon returning with ResponseHandler.
    async def select_one(self, column: list='*', condition: str=None, condition_constant: list=None):
        query = """
        SELECT {columns} FROM {table} {condition} LIMIT 1;
        """.format(
            columns=",".join(column) if isinstance(column, list) else "*",
            table=self.table_name,
            condition=("WHERE " + condition) if condition else "")
        return await Connection.fetch_one(query, *(condition_constant or []))

    
    async def update(self, update: list, update_constant: list, condition: str=None, condition_constant: list=None):
        query = "UPDATE {table} SET {update} WHERE {condition};". \
            format(table=self.table_name,
                   update=",".join(update),
                   condition=condition)
        return await Connection.execute_query(query, *update_constant, *condition_constant)


    async def delete(self, condition: str=None, condition_constant: list=None):
        query = "DELETE FROM {table} WHERE {condition} ".\
            format(table=self.table_name,
            condition= condition)
        return await Connection.execute_query(query, *condition_constant)


    async def execute_select_query(self, query: str, *args):
        return await Connection.fetch_all(query, *args)


    async def execute_select_one_query(self, query: str, *args):
        return await Connection.fetch_one(query, *args)


    async def execute_custom_query(self, query: str, *args):
        return await Connection.execute_query(query, *args)


    async def execute_batch_query(self, query: str, *args):
        return await Connection.execute_batch_query(query, *args)

