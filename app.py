import asyncio

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, DBAssignment
from constants.sql_operator import SqlOperator
from models import Users as U, Enterprise as E



dao = QueryBuilder("users")

c1 = DBCondition(term="user_id", operator=SqlOperator.NOTIN, const=[111,112])
c1.build_condition()

c2 = DBCondition(term="phone_number", operator=SqlOperator.EQL, const="sdasd")
c2.build_condition()

final_condition = c1.__or__(c2)
# dao.select_join(join_type=[], columns=[U.user_id, E.identifier], joint_table=E, join_condition="ON ..." , condition=condition, condition_const=condition)

async def main():
    await Connection.creating_pool()

    result = await dao.select(condition=final_condition.condition, condition_constant=final_condition.const, mock=False)
    print(result)


if __name__=="__main__":
    asyncio.run(main())