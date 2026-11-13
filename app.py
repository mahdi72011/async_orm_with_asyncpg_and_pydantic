import asyncio
from pydantic import BaseModel
from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, DBAssignment, ColumnCondition
from constants.sql_operator import SqlOperator
from constants.join_types import JoinType
from tables import Users as U, Enterprise as E


class Users(BaseModel):
    phone_number: str
    username: str


dao = QueryBuilder("users")

c1 = DBCondition(term=U.user_id, operator=SqlOperator.NOTIN, const=[111,112])
c1.build_condition()

c2 = DBCondition(term=U.phone_number, operator=SqlOperator.EQL, const="09110000000")
c2.build_condition()

final_condition = c1 | c2


# on = DBCondition(term=U.enterprise_id, operator=SqlOperator.EQL, const=E.id)
# on.build_condition()
on = ColumnCondition(base_term=U.enterprise_id, operator=SqlOperator.EQL, join_term=E.id)
on.build_condition()

final_on = c1 | on | c2

# up = DBAssignment({"username": "hasssan", "address": "tehran"})
# up.build_assignment()
user = Users(phone_number="09111000000", username="mahdi")

async def main():
    await Connection.creating_pool()
    result = await dao.select_join(column=[U.user_id, E.identifier],join_type=JoinType.LEFT, join_table=E, on=final_on, db_condition=final_condition)
    # result = await dao.select_one(condition=final_condition)
    # result = await dao.upsert_row(base_model=user, conflict="phone_number", action="UPDATE", update=up, condition=c2, returning_column=[U.user_id])
    print(result)


if __name__=="__main__":
    asyncio.run(main())