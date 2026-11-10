import asyncio

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, DBAssignment, JoinCondition
from constants.sql_operator import SqlOperator
from constants.join_types import JoinType
from models import Users as U, Enterprise as E



dao = QueryBuilder("users")

c1 = DBCondition(term="user_id", operator=SqlOperator.NOTIN, const=[111,112])
c1.build_condition()

c2 = DBCondition(term="phone_number", operator=SqlOperator.EQL, const="sdasd")
c2.build_condition()

final_condition = c1 | c2

on = JoinCondition(base_term=U.enterprise_id, operator=SqlOperator.EQL, join_term=E.id)
on.build_join_condition()

# up = DBAssignment({"username": "hassan", "address": "tehran"})
# up.build_assignment()




async def main():
    await Connection.creating_pool()
    result = await dao.select_join(column=[U.user_id, E.identifier],join_type=JoinType.LEFT, join_table=E, on=on, db_condition=final_condition)
    # result = await dao.select_one(condition=final_condition)
    print(result)


if __name__=="__main__":
    asyncio.run(main())