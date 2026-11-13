import pytest

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, ColumnCondition
from constants.sql_operator import SqlOperator
from constants.join_types import JoinType, JoinOn
from tables import Actor, Film, FilmActor


@pytest.mark.asyncio
async def test_select_multi_join_actor():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor.actor_id, film_actor.film_id, film.title
        FROM actor
        LEFT JOIN film_actor
            ON (actor.actor_id = film_actor.actor_id AND film_actor.film_id > $1)
        INNER JOIN film
            ON film_actor.film_id = film.film_id
        WHERE actor.actor_id > $2
        ORDER BY actor.actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 100, 5)

    # First JOIN condition
    c1 = ColumnCondition(
        base_term=Actor.actor_id,
        operator=SqlOperator.EQL,
        join_term=FilmActor.actor_id
    )

    c2 = DBCondition(
        term=FilmActor.film_id,
        operator=SqlOperator.GT,
        const=100
    )

    on1 = c1 & c2

    # Second JOIN condition
    c3 = ColumnCondition(
        base_term=FilmActor.film_id,
        operator=SqlOperator.EQL,
        join_term=Film.film_id
    )

    on2 = c3

    join1 = JoinOn(JoinType.LEFT, FilmActor, on1)
    join2 = JoinOn(JoinType.INNER, Film, on2)
    join_on_list = [join1, join2]

    condition = DBCondition(
        term=Actor.actor_id,
        operator=SqlOperator.GT,
        const=5
    )

    actual = await dao.select_multi_join(
        column=[
            Actor.actor_id,
            FilmActor.film_id,
            Film.title
        ],
        join_on_list=join_on_list,
        db_condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]