from enum import StrEnum
from tables import TableDefinition
from db.condition import ColumnCondition



class JoinType(StrEnum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"


class JoinDefinition:
    def __init__(self, join_type: JoinType, join_table: type[TableDefinition], on: ColumnCondition):
        self.join_type = join_type
        self.join_table = join_table
        self.on = on