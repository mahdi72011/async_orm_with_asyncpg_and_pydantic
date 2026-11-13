from enum import StrEnum

from tables import TableDefinition
from db.condition import ColumnCondition



class JoinType(StrEnum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"


class JoinOn:
    def __init__(self, join_type: JoinType, join_table: type[TableDefinition], on: ColumnCondition):
        self.join_type = join_type
        self.join_table = join_table
        self.on = on

    @property
    def join_table(self) -> str:
        return self._join_table

    @join_table.setter
    def join_table(self, table: type[TableDefinition]):
        self._join_table = table.__table_name__

