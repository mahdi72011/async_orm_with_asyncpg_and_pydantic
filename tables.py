from enum import StrEnum
from typing import Protocol



class TableDefinition(Protocol):
    __table_name__: str
    __alias__: str


class Users(StrEnum):
    __table_name__ = "users"
    __alias__ = "u"

    user_id        = "users.user_id"
    username       = "users.username"
    phone_number   = "users.phone_number"
    address        = "users.address"
    is_blacklisted = "users.is_blacklisted"
    created_at     = "users.created_at"
    updated_at     = "users.updated_at"
    family_name    = "users.family_name"
    first_name     = "users.first_name"
    enterprise_id  = "users.enterprise_id"
    enterprise_role = "users.enterprise_role"


class Enterprise(StrEnum):
    __table_name__ = "enterprise"
    __alias__ = "e"

    id         = "enterprise.id"
    name       = "enterprise.name"
    address    = "enterprise.address"
    identifier = "enterprise.identifier"
    updated_at = "enterprise.updated_at"


class Orders(StrEnum):
    __table_name__ = "orders"
    __alias__ = "o"

    order_id              = "orders.order_id"
    user_id               = "orders.user_id"
    source_channel        = "orders.source_channel"
    source_channel_id     = "orders.source_channel_id"
    delivery_address      = "orders.delivery_address"
    scheduled_delivery_at = "orders.scheduled_delivery_at"
    order_status          = "orders.order_status"
    payment_status        = "orders.payment_status"
    created_at            = "orders.created_at"
    updated_at            = "orders.updated_at"
    enterprise            = "orders.enterprise"
    user_query            = "orders.user_query"
    version               = "orders.version"
    admin_id              = "orders.admin_id"
    enterprise_id         = "orders.enterprise_id"


from enum import StrEnum


class Actor(StrEnum):
    __table_name__ = "actor"
    __alias__ = "a"

    actor_id = "actor.actor_id"
    first_name = "actor.first_name"
    last_name = "actor.last_name"
    last_update = "actor.last_update"


class Address(StrEnum):
    __table_name__ = "address"
    __alias__ = "ad"

    address_id = "address.address_id"
    address = "address.address"
    address2 = "address.address2"
    district = "address.district"
    city_id = "address.city_id"
    postal_code = "address.postal_code"
    phone = "address.phone"
    last_update = "address.last_update"


class Category(StrEnum):
    __table_name__ = "category"
    __alias__ = "cat"

    category_id = "category.category_id"
    name = "category.name"
    last_update = "category.last_update"


class City(StrEnum):
    __table_name__ = "city"
    __alias__ = "ci"

    city_id = "city.city_id"
    city = "city.city"
    country_id = "city.country_id"
    last_update = "city.last_update"


class Country(StrEnum):
    __table_name__ = "country"
    __alias__ = "co"

    country_id = "country.country_id"
    country = "country.country"
    last_update = "country.last_update"


class Customer(StrEnum):
    __table_name__ = "customer"
    __alias__ = "cu"

    customer_id = "customer.customer_id"
    store_id = "customer.store_id"
    first_name = "customer.first_name"
    last_name = "customer.last_name"
    email = "customer.email"
    address_id = "customer.address_id"
    activebool = "customer.activebool"
    create_date = "customer.create_date"
    last_update = "customer.last_update"
    active = "customer.active"


class Film(StrEnum):
    __table_name__ = "film"
    __alias__ = "f"

    film_id = "film.film_id"
    title = "film.title"
    description = "film.description"
    release_year = "film.release_year"
    language_id = "film.language_id"
    rental_duration = "film.rental_duration"
    rental_rate = "film.rental_rate"
    length = "film.length"
    replacement_cost = "film.replacement_cost"
    rating = "film.rating"
    last_update = "film.last_update"
    special_features = "film.special_features"
    fulltext = "film.fulltext"


class FilmActor(StrEnum):
    __table_name__ = "film_actor"
    __alias__ = "fa"

    actor_id = "film_actor.actor_id"
    film_id = "film_actor.film_id"
    last_update = "film_actor.last_update"


class FilmCategory(StrEnum):
    __table_name__ = "film_category"
    __alias__ = "fc"

    film_id = "film_category.film_id"
    category_id = "film_category.category_id"
    last_update = "film_category.last_update"


class Inventory(StrEnum):
    __table_name__ = "inventory"
    __alias__ = "i"

    inventory_id = "inventory.inventory_id"
    film_id = "inventory.film_id"
    store_id = "inventory.store_id"
    last_update = "inventory.last_update"


class Language(StrEnum):
    __table_name__ = "language"
    __alias__ = "l"

    language_id = "language.language_id"
    name = "language.name"
    last_update = "language.last_update"


class Payment(StrEnum):
    __table_name__ = "payment"
    __alias__ = "p"

    payment_id = "payment.payment_id"
    customer_id = "payment.customer_id"
    staff_id = "payment.staff_id"
    rental_id = "payment.rental_id"
    amount = "payment.amount"
    payment_date = "payment.payment_date"


class Rental(StrEnum):
    __table_name__ = "rental"
    __alias__ = "r"

    rental_id = "rental.rental_id"
    rental_date = "rental.rental_date"
    inventory_id = "rental.inventory_id"
    customer_id = "rental.customer_id"
    return_date = "rental.return_date"
    staff_id = "rental.staff_id"
    last_update = "rental.last_update"


class Staff(StrEnum):
    __table_name__ = "staff"
    __alias__ = "st"

    staff_id = "staff.staff_id"
    first_name = "staff.first_name"
    last_name = "staff.last_name"
    address_id = "staff.address_id"
    email = "staff.email"
    store_id = "staff.store_id"
    active = "staff.active"
    username = "staff.username"
    password = "staff.password"
    last_update = "staff.last_update"
    picture = "staff.picture"


class Store(StrEnum):
    __table_name__ = "store"
    __alias__ = "str"

    store_id = "store.store_id"
    manager_staff_id = "store.manager_staff_id"
    address_id = "store.address_id"
    last_update = "store.last_update"