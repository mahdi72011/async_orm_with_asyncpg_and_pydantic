import asyncio

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, DBAssignment
from constants.sql_operator import SqlOperator




sql_factory = QueryBuilder("users")

condition = DBCondition(term="user_id", operator=SqlOperator.NOTIN, const=[111,112])
condition.build_condition()


async def main():
    await Connection.creating_pool()

    result = await sql_factory.select(condition=condition.condition, condition_constant=condition.const, mock=False)
    print(result)


if __name__=="__main__":
    asyncio.run(main())