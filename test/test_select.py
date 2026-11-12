import pytest

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition
from constants.sql_operator import SqlOperator
from models import Orders, Enterprise, Users





@pytest.mark.asyncio
async def test_select_order():
    await Connection.creating_pool()
    dao = QueryBuilder("orders")

    order_id = 100
    query ="""
            SELECT order_id, user_id, enterprise_id, delivery_address
            FROM orders
            WHERE order_id = $1
            ;
        """
    expected = await dao.execute_select_query(query, order_id)

    c = DBCondition(term=Orders.order_id, operator=SqlOperator.EQL, const=order_id)
    c.build_condition()
    actual = await dao.select(
        column=[Orders.order_id, Orders.user_id, Orders.enterprise_id, Orders.delivery_address],
        condition=c
    )
    assert expected is not None
    assert [dict(row) for row in actual] == [dict(row) for row in expected]






@pytest.mark.asyncio
async def test_select_enterprise():
    await Connection.creating_pool()
    dao = QueryBuilder("enterprise")

    name = "Mahdi"
    excluded_id = 10

    query = """
        SELECT id
        FROM enterprise
        WHERE lower(btrim(name)) = lower($1)
          AND id IS DISTINCT FROM $2
        ORDER BY id
        LIMIT 1;
    """

    expected = await dao.execute_select_query(
        query, name, excluded_id
    )

    c1 = DBCondition(term=f"lower(btrim({Enterprise.name}))", operator=SqlOperator.LOWER_EQL, const=name)
    c1.build_condition()

    c2 = DBCondition(term=Enterprise.id, operator=SqlOperator.IS_DISTINCT_FROM, const=excluded_id)
    c2.build_condition()

    condition = c1 & c2

    actual = await dao.select(
        column=[Enterprise.id],
        condition=condition,
        order=Enterprise.id,
        limit=1
    )

    assert expected is not None
    assert [dict(row) for row in actual] == [dict(row) for row in expected]



@pytest.mark.asyncio
async def test_select_user_owner():
    await Connection.creating_pool()
    dao = QueryBuilder("users")

    enterprise_id = 10

    query = """
        SELECT 1
        FROM users x
        WHERE x.enterprise_id = $1
          AND x.enterprise_role = 'owner';
    """

    expected = await dao.execute_select_query(query, enterprise_id)

    c1 = DBCondition(term=Users.enterprise_id, operator=SqlOperator.EQL, const=enterprise_id)
    c1.build_condition()
    c2 = DBCondition(term=Users.enterprise_role, operator=SqlOperator.EQL, const="owner")
    c2.build_condition()

    condition = c1 & c2

    actual = await dao.select(
        column=["1"],
        condition=condition
    )

    assert [dict(row) for row in actual] == [dict(row) for row in expected]