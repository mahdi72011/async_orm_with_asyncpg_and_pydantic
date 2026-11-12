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