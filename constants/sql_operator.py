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
    BETWEEN = " BETWEEN "
    IN = " = ANY"
    NOTIN = " <> ALL"
