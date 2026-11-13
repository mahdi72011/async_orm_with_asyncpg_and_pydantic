from decimal import Decimal

import pytest

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, ColumnCondition
from constants.sql_operator import SqlOperator
from tables import Actor, Rental, Category, Film, Payment, Country, Customer


@pytest.mark.asyncio
async def test_select_actor():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor_id, first_name, last_name
        FROM actor
        WHERE (first_name ILIKE $1 OR last_name ILIKE $2)
          AND actor_id > $3
        ORDER BY actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "%a%", "%a%", 10)

    c1 = DBCondition(term=Actor.first_name, operator=SqlOperator.ILIKE, const="%a%")
    c2 = DBCondition(term=Actor.last_name, operator=SqlOperator.ILIKE, const="%a%")
    c3 = DBCondition(term=Actor.actor_id, operator=SqlOperator.GT, const=10)

    condition = (c1 | c2) & c3

    actual = await dao.select(
        column=[Actor.actor_id, Actor.first_name, Actor.last_name],
        condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_rental():
    await Connection.creating_pool()
    dao = QueryBuilder("rental")

    query = """
        SELECT rental_id, customer_id, inventory_id, return_date
        FROM rental
        WHERE return_date IS NULL
          AND staff_id = $1
        ORDER BY rental_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 1)

    c1 = DBCondition(term=Rental.return_date, operator=SqlOperator.NULL)
    c2 = DBCondition(term=Rental.staff_id, operator=SqlOperator.EQL, const=1)
    condition = c1 & c2

    actual = await dao.select(
        column=[Rental.rental_id, Rental.customer_id, Rental.inventory_id, Rental.return_date],
        condition=condition,
        order_by=Rental.rental_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_actor_like():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor_id, first_name, last_name
        FROM actor
        WHERE first_name LIKE $1
          AND last_name != $2
          AND actor_id < $3
        ORDER BY actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "%a%", "ZZZ", 200)

    c1 = DBCondition(term=Actor.first_name, operator=SqlOperator.LIKE, const="%a%")
    c2 = DBCondition(term=Actor.last_name, operator=SqlOperator.NOTEQL, const="ZZZ")
    c3 = DBCondition(term=Actor.actor_id, operator=SqlOperator.LT, const=200)
    condition = c1 & c2 & c3

    actual = await dao.select(
        column=[Actor.actor_id, Actor.first_name, Actor.last_name],
        condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_category_in():
    await Connection.creating_pool()
    dao = QueryBuilder("category")

    query = """
        SELECT category_id, name
        FROM category
        WHERE category_id = ANY($1)
        ORDER BY category_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, [1, 2, 3])

    condition = DBCondition(
        term=Category.category_id,
        operator=SqlOperator.IN,
        const=[1, 2, 3]
    )

    actual = await dao.select(
        column=[Category.category_id, Category.name],
        condition=condition,
        order_by=Category.category_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_category_notin():
    await Connection.creating_pool()
    dao = QueryBuilder("category")

    query = """
        SELECT category_id, name
        FROM category
        WHERE category_id <> ALL($1)
        ORDER BY category_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, [1, 2, 3])

    condition = DBCondition(
        term=Category.category_id,
        operator=SqlOperator.NOTIN,
        const=[1, 2, 3]
    )

    actual = await dao.select(
        column=[Category.category_id, Category.name],
        condition=condition,
        order_by=Category.category_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_film_between():
    await Connection.creating_pool()
    dao = QueryBuilder("film")

    query = """
        SELECT film_id, title, length
        FROM film
        WHERE length BETWEEN $1 AND $2
        ORDER BY film_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 80, 120)

    condition = DBCondition(
        term=Film.length,
        operator=SqlOperator.BETWEEN,
        const=(80, 120)
    )

    actual = await dao.select(
        column=[Film.film_id, Film.title, Film.length],
        condition=condition,
        order_by=Film.film_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_payment_amount():
    await Connection.creating_pool()
    dao = QueryBuilder("payment")

    query = """
        SELECT payment_id, customer_id, amount
        FROM payment
        WHERE amount IS NOT NULL
          AND amount >= $1
          AND amount <= $2
        ORDER BY payment_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(
        query, Decimal("3.99"), Decimal("8.99")
    )

    c1 = DBCondition(term=Payment.amount, operator=SqlOperator.NOTNULL)
    c2 = DBCondition(term=Payment.amount, operator=SqlOperator.GTE, const=Decimal("3.99"))
    c3 = DBCondition(term=Payment.amount, operator=SqlOperator.LTE, const=Decimal("8.99"))
    condition = c1 & c2 & c3

    actual = await dao.select(
        column=[Payment.payment_id, Payment.customer_id, Payment.amount],
        condition=condition,
        order_by=Payment.payment_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_country_lower():
    await Connection.creating_pool()
    dao = QueryBuilder("country")

    query = """
        SELECT country_id, country
        FROM country
        WHERE lower(btrim(country)) = lower($1)
        ORDER BY country_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "united states")

    condition = DBCondition(
        term=f"lower(btrim({Country.country}))",
        operator=SqlOperator.LOWER_EQL,
        const="united states"
    )

    actual = await dao.select(
        column=[Country.country_id, Country.country],
        condition=condition,
        order_by=Country.country_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_customer_distinct():
    await Connection.creating_pool()
    dao = QueryBuilder("customer")

    query = """
        SELECT customer_id, first_name, last_name, email
        FROM customer
        WHERE customer_id IS DISTINCT FROM $1
          AND customer_id < $2
        ORDER BY customer_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 1, 15)

    c1 = DBCondition(
        term=Customer.customer_id,
        operator=SqlOperator.IS_DISTINCT_FROM,
        const=1
    )
    c2 = DBCondition(term=Customer.customer_id, operator=SqlOperator.LT, const=15)
    condition = c1 & c2

    actual = await dao.select(
        column=[Customer.customer_id, Customer.first_name, Customer.last_name, Customer.email],
        condition=condition,
        order_by=Customer.customer_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_film_column_comparison():
    await Connection.creating_pool()
    dao = QueryBuilder("film")

    query = """
        SELECT film_id, title, rental_rate, replacement_cost, rental_duration
        FROM film
        WHERE (
            rental_rate = rental_rate
            OR rental_rate != replacement_cost
            OR rental_rate > replacement_cost
            OR rental_rate >= replacement_cost
            OR rental_rate < replacement_cost
            OR rental_rate <= replacement_cost
        )
        AND rental_duration >= $1
        ORDER BY film_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 5)

    c1 = ColumnCondition(Film.rental_rate, SqlOperator.EQL, Film.rental_rate)
    c2 = ColumnCondition(Film.rental_rate, SqlOperator.NOTEQL, Film.replacement_cost)
    c3 = ColumnCondition(Film.rental_rate, SqlOperator.GT, Film.replacement_cost)
    c4 = ColumnCondition(Film.rental_rate, SqlOperator.GTE, Film.replacement_cost)
    c5 = ColumnCondition(Film.rental_rate, SqlOperator.LT, Film.replacement_cost)
    c6 = ColumnCondition(Film.rental_rate, SqlOperator.LTE, Film.replacement_cost)

    column_condition = c1 | c2 | c3 | c4 | c5 | c6

    c7 = DBCondition(
        term=Film.rental_duration,
        operator=SqlOperator.GTE,
        const=5
    )
    condition = column_condition & c7

    actual = await dao.select(
        column=[
            Film.film_id,
            Film.title,
            Film.rental_rate,
            Film.replacement_cost,
            Film.rental_duration
        ],
        condition=condition,
        order_by=Film.film_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]