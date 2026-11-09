from enum import StrEnum



class SqlOperator(StrEnum):

    EQL = "="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    NOTEQL = "!="
    LIKE = " LIKE "
    ILIKE = " ILIKE "
    IN = " = ANY"
    NOTIN = " <> ALL"
    BETWEEN = " BETWEEN "


