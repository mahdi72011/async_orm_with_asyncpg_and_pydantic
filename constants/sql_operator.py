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
    LOWER_EQL = " = lower(${}) "
    IS_DISTINCT_FROM = " IS DISTINCT FROM " + "(${}) "

    @property
    def column_operator(self):
        operators = {
            SqlOperator.EQL: " = ",
            SqlOperator.NOTEQL: " != ",
            SqlOperator.GT: " > ",
            SqlOperator.GTE: " >= ",
            SqlOperator.LT: " < ",
            SqlOperator.LTE: " <= ",
        }
        if self not in operators:
            raise ValueError(f"{self.name} cannot be used for column comparison")

        return operators[self]

    
    def operator_argument(self, value):
        
        operator_constants = {
            SqlOperator.EQL: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.GT: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.GTE: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.LT: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.LTE: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.NOTEQL: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.LIKE: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.ILIKE: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.IN: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.NOTIN: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.BETWEEN: value,
            SqlOperator.NULL: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.NOTNULL: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.LOWER_EQL: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
            SqlOperator.IS_DISTINCT_FROM: () if value is None else (list(value),) if isinstance(value, (list, tuple)) else (value,),
        }

        return operator_constants[self]
