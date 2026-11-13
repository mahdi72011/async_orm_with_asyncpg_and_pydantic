import pytest

from db.connection import Connection
from db.query_builder import QueryBuilder
from db.condition import DBCondition, ColumnCondition
from constants.sql_operator import SqlOperator
from constants.join_types import JoinType
from tables import Actor, Address, Category, City, Country, Customer, Film, FilmActor, FilmCategory, Inventory, Language, Payment, Rental


@pytest.mark.asyncio
async def test_select_join_actor11():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor.actor_id, film_actor.film_id
        FROM actor
        LEFT JOIN film_actor
            ON (actor.actor_id = film_actor.actor_id AND film_actor.film_id > $1)
        WHERE actor.actor_id > $2
        ORDER BY actor.actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 100, 5)

    c1 = ColumnCondition(base_term=Actor.actor_id, operator=SqlOperator.EQL, join_term=FilmActor.actor_id)
    c2 = DBCondition(term=FilmActor.film_id, operator=SqlOperator.GT, const=100)

    on = c1 & c2

    condition = DBCondition(term=Actor.actor_id, operator=SqlOperator.GT, const=5)

    actual = await dao.select_join(
        column=[Actor.actor_id, FilmActor.film_id],
        join_type=JoinType.LEFT,
        join_table=FilmActor,
        on=on,
        db_condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_actor2():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor.actor_id, film_actor.film_id
        FROM actor
        LEFT JOIN film_actor ON actor.actor_id = film_actor.actor_id
        WHERE actor.actor_id > $1
        ORDER BY actor.actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 10)

    on = ColumnCondition(base_term=Actor.actor_id, operator=SqlOperator.EQL, join_term=FilmActor.actor_id)

    condition = DBCondition(term=Actor.actor_id, operator=SqlOperator.GT, const=10)

    actual = await dao.select_join(
        column=[Actor.actor_id, FilmActor.film_id],
        join_type=JoinType.LEFT,
        join_table=FilmActor,
        on=on,
        db_condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]

@pytest.mark.asyncio
async def test_select_join_film_language():
    await Connection.creating_pool()
    dao = QueryBuilder("film")

    query = """
        SELECT film.film_id, film.title, language.name
        FROM film
        INNER JOIN language ON film.language_id = language.language_id
        WHERE film.rental_rate > $1
        ORDER BY film.film_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 2.99)

    on = ColumnCondition(base_term=Film.language_id, operator=SqlOperator.EQL, join_term=Language.language_id)

    condition = DBCondition(term=Film.rental_rate, operator=SqlOperator.GT, const=2.99)

    actual = await dao.select_join(
        column=[Film.film_id, Film.title, Language.name],
        join_type=JoinType.INNER,
        join_table=Language,
        on=on,
        db_condition=condition,
        order_by=Film.film_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_customer_address():
    await Connection.creating_pool()
    dao = QueryBuilder("customer")

    query = """
        SELECT customer.customer_id, customer.first_name, address.address
        FROM customer
        LEFT JOIN address ON customer.address_id = address.address_id
        WHERE customer.active = $1
        ORDER BY customer.customer_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, True)

    on = ColumnCondition(base_term=Customer.address_id, operator=SqlOperator.EQL, join_term=Address.address_id)

    condition = DBCondition(term=Customer.active, operator=SqlOperator.EQL, const=True)

    actual = await dao.select_join(
        column=[Customer.customer_id, Customer.first_name, Address.address],
        join_type=JoinType.LEFT,
        join_table=Address,
        on=on,
        db_condition=condition,
        order_by=Customer.customer_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_address_city():
    await Connection.creating_pool()
    dao = QueryBuilder("address")

    query = """
        SELECT address.address_id, address.address, city.city
        FROM address
        INNER JOIN city ON address.city_id = city.city_id
        WHERE city.city ILIKE $1
        ORDER BY address.address_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "%a%")

    on = ColumnCondition(base_term=Address.city_id, operator=SqlOperator.EQL, join_term=City.city_id)

    condition = DBCondition(term=City.city, operator=SqlOperator.ILIKE, const="%a%")

    actual = await dao.select_join(
        column=[Address.address_id, Address.address, City.city],
        join_type=JoinType.INNER,
        join_table=City,
        on=on,
        db_condition=condition,
        order_by=Address.address_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_city_country():
    await Connection.creating_pool()
    dao = QueryBuilder("city")

    query = """
        SELECT city.city_id, city.city, country.country
        FROM city
        INNER JOIN country ON city.country_id = country.country_id
        WHERE country.country ILIKE $1
        ORDER BY city.city_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "a%")

    on = ColumnCondition(base_term=City.country_id, operator=SqlOperator.EQL, join_term=Country.country_id)

    condition = DBCondition(term=Country.country, operator=SqlOperator.ILIKE, const="a%")

    actual = await dao.select_join(
        column=[City.city_id, City.city, Country.country],
        join_type=JoinType.INNER,
        join_table=Country,
        on=on,
        db_condition=condition,
        order_by=City.city_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_film_film_actor():
    await Connection.creating_pool()
    dao = QueryBuilder("film")

    query = """
        SELECT film.film_id, film.title, film_actor.actor_id
        FROM film
        LEFT JOIN film_actor ON film.film_id = film_actor.film_id
        WHERE film.length > $1
        ORDER BY film.film_id ASC, film_actor.actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 120)

    on = ColumnCondition(base_term=Film.film_id, operator=SqlOperator.EQL, join_term=FilmActor.film_id)

    condition = DBCondition(term=Film.length, operator=SqlOperator.GT, const=120)

    actual = await dao.select_join(
        column=[Film.film_id, Film.title, FilmActor.actor_id],
        join_type=JoinType.LEFT,
        join_table=FilmActor,
        on=on,
        db_condition=condition,
        order_by=f"{Film.film_id}, {FilmActor.actor_id}",
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_category_film_category():
    await Connection.creating_pool()
    dao = QueryBuilder("category")

    query = """
        SELECT category.category_id, category.name, film_category.film_id
        FROM category
        INNER JOIN film_category ON category.category_id = film_category.category_id
        WHERE category.name ILIKE $1
        ORDER BY category.category_id ASC, film_category.film_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, "%action%")

    on = ColumnCondition(base_term=Category.category_id, operator=SqlOperator.EQL, join_term=FilmCategory.category_id)

    condition = DBCondition(term=Category.name, operator=SqlOperator.ILIKE, const="%action%")

    actual = await dao.select_join(
        column=[Category.category_id, Category.name, FilmCategory.film_id],
        join_type=JoinType.INNER,
        join_table=FilmCategory,
        on=on,
        db_condition=condition,
        order_by=f"{Category.category_id}, {FilmCategory.film_id}",
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_inventory_film():
    await Connection.creating_pool()
    dao = QueryBuilder("inventory")

    query = """
        SELECT inventory.inventory_id, inventory.store_id, film.film_id, film.title
        FROM inventory
        INNER JOIN film ON inventory.film_id = film.film_id
        WHERE inventory.store_id = $1
        ORDER BY inventory.inventory_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 1)

    on = ColumnCondition(base_term=Inventory.film_id, operator=SqlOperator.EQL, join_term=Film.film_id)

    condition = DBCondition(term=Inventory.store_id, operator=SqlOperator.EQL, const=1)

    actual = await dao.select_join(
        column=[Inventory.inventory_id, Inventory.store_id, Film.film_id, Film.title],
        join_type=JoinType.INNER,
        join_table=Film,
        on=on,
        db_condition=condition,
        order_by=Inventory.inventory_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_rental_customer():
    await Connection.creating_pool()
    dao = QueryBuilder("rental")

    query = """
        SELECT rental.rental_id, rental.customer_id, customer.first_name
        FROM rental
        INNER JOIN customer ON rental.customer_id = customer.customer_id
        WHERE rental.return_date IS NULL
        ORDER BY rental.rental_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query)

    on = ColumnCondition(base_term=Rental.customer_id, operator=SqlOperator.EQL, join_term=Customer.customer_id)

    condition = DBCondition(term=Rental.return_date, operator=SqlOperator.NULL)

    actual = await dao.select_join(
        column=[Rental.rental_id, Rental.customer_id, Customer.first_name],
        join_type=JoinType.INNER,
        join_table=Customer,
        on=on,
        db_condition=condition,
        order_by=Rental.rental_id,
        asc_or_desc="ASC",
        limit=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_payment_customer():
    await Connection.creating_pool()
    dao = QueryBuilder("payment")

    query = """
        SELECT payment.payment_id, payment.customer_id, payment.amount, customer.first_name
        FROM payment
        INNER JOIN customer ON payment.customer_id = customer.customer_id
        WHERE (payment.amount > $1 AND payment.customer_id > $2)
        ORDER BY payment.payment_id DESC
        LIMIT 10 OFFSET 10;
    """

    expected = await dao.execute_select_query(query, 5, 10)

    c1 = DBCondition(term=Payment.amount, operator=SqlOperator.GT, const=5)
    c2 = DBCondition(term=Payment.customer_id, operator=SqlOperator.GT, const=10)

    condition = c1 & c2

    on = ColumnCondition(base_term=Payment.customer_id, operator=SqlOperator.EQL, join_term=Customer.customer_id)

    actual = await dao.select_join(
        column=[Payment.payment_id, Payment.customer_id, Payment.amount, Customer.first_name],
        join_type=JoinType.INNER,
        join_table=Customer,
        on=on,
        db_condition=condition,
        order_by=Payment.payment_id,
        asc_or_desc="DESC",
        limit=10,
        offset=10
    )

    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]


@pytest.mark.asyncio
async def test_select_join_actor():
    await Connection.creating_pool()
    dao = QueryBuilder("actor")

    query = """
        SELECT actor.actor_id, film_actor.film_id
        FROM actor
        LEFT JOIN film_actor
            ON (actor.actor_id = film_actor.actor_id AND film_actor.film_id > $1)
        WHERE actor.actor_id > $2
        ORDER BY actor.actor_id ASC
        LIMIT 10;
    """

    expected = await dao.execute_select_query(query, 100, 5)

    c1 = ColumnCondition(base_term=Actor.actor_id, operator=SqlOperator.EQL, join_term=FilmActor.actor_id)
    c2 = DBCondition(term=FilmActor.film_id, operator=SqlOperator.GT, const=100)

    on = c1 & c2

    condition = DBCondition(term=Actor.actor_id, operator=SqlOperator.GT, const=5)

    actual = await dao.select_join(
        column=[Actor.actor_id, FilmActor.film_id],
        join_type=JoinType.LEFT,
        join_table=FilmActor,
        on=on,
        db_condition=condition,
        order_by=Actor.actor_id,
        asc_or_desc="ASC",
        limit=10
    )
    print(11111111111111111, flush=True)
    assert expected
    assert [dict(row) for row in actual] == [
        dict(row) for row in expected
    ]