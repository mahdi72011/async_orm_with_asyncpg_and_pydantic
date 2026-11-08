from enum import Enum



class SqlOperator(Enum):

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

