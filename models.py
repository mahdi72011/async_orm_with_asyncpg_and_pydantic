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


class Enterprise(StrEnum):
    __table_name__ = "enterprise"
    __alias__ = "e"

    id         = "enterprise.id"
    name       = "enterprise.name"
    address    = "enterprise.address"
    identifier = "enterprise.identifier"
    updated_at = "enterprise.updated_at"