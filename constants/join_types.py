from enum import StrEnum
from tables import TableDefinition
from db.condition import ColumnCondition



class JoinType(StrEnum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"
