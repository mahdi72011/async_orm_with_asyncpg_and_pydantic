from enum import StrEnum
from typing import Protocol



class TableDefinition(Protocol):
    __table_name__: str
    __alias__: str


class Users(StrEnum):
    __table_name__ = "users"
    __alias__ = "u"

    user_id        = "u.user_id"
    username       = "u.username"
    phone_number   = "u.phone_number"
    address        = "u.address"
    is_blacklisted = "u.is_blacklisted"
    created_at     = "u.created_at"
    updated_at     = "u.updated_at"
    family_name    = "u.family_name"
    first_name     = "u.first_name"
    enterprise_id  = "u.enterprise_id"


class Enterprise(StrEnum):
    __table_name__ = "enterprise"
    __alias__ = "e"

    id         = "e.id"
    name       = "e.name"
    address    = "e.address"
    identifier = "e.identifier"
    updated_at = "e.updated_at"