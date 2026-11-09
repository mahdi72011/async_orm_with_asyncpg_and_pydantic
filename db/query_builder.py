from pydantic import BaseModel
from typing import List

from db.connection import Connection
from db.condition import DBCondition, DBAssignment
from constants.join_types import JoinType
from models import TableDefinition

class QueryBuilder:
    def __init__(self, table_name: str, alias: str=None):
        self.table_name = table_name
        self.alias = alias if alias else table_name[0].lower()


    def compile_update_clauses(self, update: DBAssignment, condition: DBCondition):
        a = len(condition.const)
        b = len(update.value_list)
        update.update_query = ",".join(update.update_list)
        update_query = update.update_query.format(*range(1,b+1))
        condition_query = condition.condition.format(*range(b+1,b+a+1))
        return update_query, condition_query

    def compile_conditions(self, condition: DBCondition):
        if not condition:
            return None
        a = len(condition.const)
        return condition.condition.format(*range(1,a+1))

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
    

    async def select(self, column: List='*', condition: DBCondition=None, group: list=None, order: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None, mock: bool=False):
        condition_query = self.compile_conditions(condition)
        query = "SELECT {columns} FROM {table} {condition} {group} {order} {asc_or_desc} {limit} {offset}".\
        format(columns=",".join(list(column)) if type(column) == list else "*",
               table=self.table_name,
               condition=("WHERE " + condition_query) if condition_query else "",
                group="GROUP BY " + ",".join(group) if group else "",
                order="ORDER BY " + order if order else "",
                asc_or_desc=asc_or_desc if asc_or_desc else "",
                limit="LIMIT " + str(limit) if limit else "",
                offset="OFFSET " + str(offset) if offset else "")
        if mock:
            return query
        return await Connection.fetch_all(query, *condition.const if condition else ())


    ### returns a record that automatically converts into json by fastapi upon returning with ResponseHandler.
    async def select_one(self, column: list='*', condition: DBCondition=None):
        condition_query = self.compile_conditions(condition)
        query = """
        SELECT {columns} FROM {table} {condition} LIMIT 1;
        """.format(
            columns=",".join(column) if isinstance(column, list) else "*",
            table=self.table_name,
            condition=("WHERE " + condition_query) if condition_query else "")
        # breakpoint()
        return await Connection.fetch_one(query, *condition.const if condition else ())

    
    async def update(self, update: DBAssignment, condition: DBCondition):
        update_query, condition_query = self.compile_update_clauses(update, condition)
        query = "UPDATE {table} SET {update} WHERE {condition};". \
            format(table=self.table_name,
                   update=update_query,
                   condition=condition_query)
        return await Connection.execute_query(query, *update.value_list, *condition.const)


    async def delete(self, condition: DBCondition):
        condition_query = self.compile_conditions(condition)
        query = "DELETE FROM {table} WHERE {condition} ".\
            format(table=self.table_name,
            condition= condition_query)
        return await Connection.execute_query(query, *condition.const)


    async def execute_select_query(self, query: str, *args):
        return await Connection.fetch_all(query, *args)


    async def execute_select_one_query(self, query: str, *args):
        return await Connection.fetch_one(query, *args)


    async def execute_custom_query(self, query: str, *args):
        return await Connection.execute_query(query, *args)


    async def execute_batch_query(self, query: str, *args):
        return await Connection.execute_batch_query(query, *args)


    async def select_join(self, column: List, join_type: JoinType, join_table: TableDefinition, on: DBCondition, db_condition: DBCondition=None, group_by: List=None, order_by: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None):
        query = """
            SELECT {columns} FROM {table_name} AS {base_alias} {join_type} {join_table_name} AS {join_alias} ON {on} {condition} {group} {order} {asc_or_desc} {limit} {offset}
            """.format(
                columns = ",".join(list(column)),
                table_name = self.table_name,
                base_alias = self.alias,
                join_type = join_type,
                join_table_name = join_table.__table_name__,
                join_alias = join_table.__alias__,
                on = on.condition,
                condition=("WHERE " + db_condition.condition) if db_condition else "",
                group="GROUP BY " + ",".join(list(group_by)) if group_by else "",
                order="ORDER BY " + order_by if order_by else "",
                asc_or_desc=asc_or_desc if asc_or_desc else "",
                limit = "LIMIT " + str(limit) if limit is not None else "",
                offset = "OFFSET " + str(offset) if offset is not None else ""
            )
        return await Connection.fetch_all(query, *on.const, *db_condition.const)

