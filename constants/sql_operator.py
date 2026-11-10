from enum import StrEnum



class SqlOperator(StrEnum):

    EQL = " = " + "(${}) "
    GT = " > " + "(${}) "
    GTE = " >= " + "(${}) "
    LT = " < " + "(${}) "
    LTE = " <= " + "(${}) "
    NOTEQL = "!= " + "(${}) "
    LIKE = " LIKE " + "(${}) "
    ILIKE = " ILIKE " + "(${}) "
    IN = " = ANY " + "(${}) "
    NOTIN = " <> ALL " + "(${}) "
    BETWEEN = " BETWEEN " + "(${}) " "AND " + "(${}) "
    NULL = " IS NULL "
    NOTNULL = " IS NOT NULL "

    @property
    def column_operator(self):
        operators = {
            SqlOperator.EQL: "=",
            SqlOperator.NOTEQL: "!=",
            SqlOperator.GT: ">",
            SqlOperator.GTE: ">=",
            SqlOperator.LT: "<",
            SqlOperator.LTE: "<=",
        }
        if self not in operators:
            raise ValueError(f"{self.name} cannot be used for column comparison")

        return operators[self]
