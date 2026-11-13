from pydantic import BaseModel
from typing import List, Literal

from db.connection import Connection
from db.condition import DBCondition, DBAssignment, ColumnCondition
from constants.join_types import JoinType, JoinOn
from tables import TableDefinition

class QueryBuilder:
    def __init__(self, table_name: str, alias: str=None):
        self.table_name = table_name
        self.alias = alias if alias else table_name[0].lower()

    # TO DO aggregate, select for update, distinct, having.

    def compile_update_clauses(self, update: DBAssignment, condition: DBCondition=None):
        b = len(update.value_list)
        update.update_query = ",".join(update.update_list)
        update_query = update.update_query.format(*range(1,b+1))
        condition_query = None
        if condition:
            a = len(condition.const)
            condition_query = condition.condition.format(*range(b+1,b+a+1))
        return update_query, condition_query

    def compile_conditions(self, condition: DBCondition, a: int=1):
        if not condition:
            return None
        condition.build_condition()
        b = len(condition.const) + a
        return condition.condition.format(*range(a,b))

    def compile_on_db_condition(self, on: ColumnCondition, condition: DBCondition=None):
        if not on:
            raise ValueError("select join query must have a join condition")
        on.build_condition()
        on_query = on.condition
        a = 1
        if getattr(on, "const", None):
            a = len(on.const) + 1
            on_query = on.condition.format(*range(1, a))
        condition_query = None
        b = 0
        if condition:
            condition.build_condition()
            b = len(condition.const)
            condition_query = condition.condition.format(*range(a,a+b))
        return on_query, condition_query

    def compile_on_condition(self, on: ColumnCondition, a: int=1):
        if not on:
            raise ValueError("select join query must have a join condition")
        on.build_condition()
        on_query = on.condition

        b = a
        if getattr(on, "const", None):
            b = len(on.const) + 1
            on_query = on.condition.format(*range(a, b))
        return on_query, b


    async def insert_row(self, base_model: BaseModel, returning_column: List[str] | None = None):
        query = "INSERT INTO {table} ({columns}) VALUES ({values}) {return_column};".\
        format(table=self.table_name,
               columns = ",".join(list(base_model.model_dump().keys())),
               values = ",".join([f"(${n + 1})" for n in range(len(base_model.model_dump().values()))]),
               return_column = ("RETURNING " + ",".join(returning_column)) if returning_column else "")
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
        return await Connection.execute_batch_query(query, [tuple(data_model.model_dump().values()) for data_model in data_models])


    async def upsert_row(self, base_model: BaseModel, conflict: str, action: Literal["UPDATE","NOTHING"]="NOTHING", update: DBAssignment=None, condition: DBCondition=None, returning_column: List[str] | None = None):
        if action == "UPDATE" and update is None:
            raise ValueError("UPDATE action requires an update assignment")
        if action == "UPDATE":
            action_query, starting_index = self.make_update_query(update, condition)
        else:
            action_query = None
            starting_index = 1
        data = base_model.model_dump()
        query = "INSERT INTO {table} ({columns}) VALUES ({values}) ON CONFLICT ({conflict}) DO {do} {action} {return_column};".\
        format(table=self.table_name,
               columns = ",".join(list(data.keys())),
               values = ",".join([f"(${starting_index + n})" for n in range(len(data.values()))]),
               conflict = conflict,
               do = action,
               action = action_query if action_query else "",
               return_column = "RETURNING " + ",".join(returning_column) if returning_column and action else "")
        print(query)

        up_params = ()
        c_params = ()
        if action == "UPDATE":
            up_params = tuple(update.value_list) if update else ()
            c_params = tuple(condition.const) if condition else ()
        if returning_column:
            return await Connection.fetch_one(query, *up_params, *c_params, *data.values())

        return await Connection.execute_query(query, *up_params, *c_params, *data.values())



    async def select(self, column: List='*', condition: DBCondition=None, group_by: list=None, order_by: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None, mock: bool=False):
        condition_query = self.compile_conditions(condition)
        query = "SELECT {columns} FROM {table} {condition} {group} {order} {asc_or_desc} {limit} {offset} ;".\
        format(columns=",".join(list(column)) if type(column) == list else "*",
               table=self.table_name,
               condition=("WHERE " + condition_query) if condition_query else "",
                group="GROUP BY " + ",".join(group_by) if group_by else "",
                order="ORDER BY " + order_by if order_by else "",
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

    def make_update_query(self, update: DBAssignment, condition: DBCondition=None):
        update_query, condition_query = self.compile_update_clauses(update, condition)
        query = "SET {update} {condition}". \
            format(update=update_query,
                   condition="WHERE " + condition_query if condition_query else "")
        n = (len(condition.const) if condition else 0) + len(update.value_list) +1
        return query, n


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


    async def select_join(self, column: List[str], join_type: JoinType, join_table: type[TableDefinition], on: ColumnCondition, db_condition: DBCondition=None, group_by: List=None, order_by: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None):
        on_query, condition_query = self.compile_on_db_condition(on, db_condition)
        query = """
            SELECT {columns} FROM {table_name} {join_type} {join_table_name} ON {on} {condition} {group} {order} {asc_or_desc} {limit} {offset}
            """.format(
                columns = ",".join(list(column)),
                table_name = self.table_name,
                join_type = join_type,
                join_table_name = join_table.__table_name__,
                on = on_query,
                condition=("WHERE " + condition_query) if condition_query else "",
                group="GROUP BY " + ",".join(list(group_by)) if group_by else "",
                order="ORDER BY " + order_by if order_by else "",
                asc_or_desc=asc_or_desc if asc_or_desc and order_by else "",
                limit = "LIMIT " + str(limit) if limit is not None else "",
                offset = "OFFSET " + str(offset) if offset is not None else ""
            )

        return await Connection.fetch_all(query, *on.const if getattr(on, "const", None) else (), *db_condition.const if db_condition else ())


    def _param(self, const):
        if isinstance(const, (list, tuple)):
            if len(const) == 1:
                return const[0]
            if len(const) == 0:
                return None
        return const

    async def select_multi_join(self, column: List[str], join_on_list: List[JoinOn], db_condition: DBCondition=None, group_by: List=None, order_by: str=None, asc_or_desc: str=None, limit: int=None, offset: int=None):
        join_query = ""
        n = 1
        for join_on in join_on_list:
            on_query, n = self.compile_on_condition(join_on.on, n)
            join_query = join_query + join_on.join_type + " " + join_on.join_table + " ON " + on_query + " "

        condition_query = self.compile_conditions(db_condition, n)

        query = """
            SELECT {columns} FROM {table_name} {join_query} {condition} {group} {order} {asc_or_desc} {limit} {offset}
            """.format(
                columns = ",".join(list(column)),
                table_name = self.table_name,
                join_query = join_query,
                condition=("WHERE " + condition_query) if condition_query else "",
                group="GROUP BY " + ",".join(list(group_by)) if group_by else "",
                order="ORDER BY " + order_by if order_by else "",
                asc_or_desc=asc_or_desc if asc_or_desc and order_by else "",
                limit = "LIMIT " + str(limit) if limit is not None else "",
                offset = "OFFSET " + str(offset) if offset is not None else ""
            )
        # params = tuple(getattr(join_on.on, "const", []) for join_on in join_on_list)
        # params = tuple(value for join_on in join_on_list for value in getattr(join_on.on, "const", ()))
        # lst = []
        # params= tuple(lst.append(list(getattr(join_on.on, "const", []))) for join_on in join_on_list)
        # params = tuple(lst)
        # print(params)
        # cd = join_on_list[0].on
        # lst = list(getattr(cd, "const", []))
        # t = tuple([].append(lst))
        # breakpoint()
        params = tuple(
        p for p in (self._param(getattr(j.on, "const", [])) for j in join_on_list)
        if p is not None
        )

        return await Connection.fetch_all(query, *params if params is not None else (), *db_condition.const if db_condition else ())
