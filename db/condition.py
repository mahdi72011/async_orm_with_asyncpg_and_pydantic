from constants.sql_operator import SqlOperator
from typing import Any


class BaseCon:
    def __init__(self):
        self.number = 1


### u.user_id = 111
class DBCondition:
    def __init__(self, term: str=None, operator: SqlOperator=None, const: Any=None):
        self.term = term
        self.operator = operator
        self.condition = ""
        self.const = () if const is None else (list(const),) if isinstance(const, (list, tuple)) else (const,)

    def build_condition(self):
        self.condition = self.term + self.operator
        return self.condition

    def __and__(self, other):
        and_condition = DBCondition()
        and_condition.const=self.const + other.const 
        and_condition.condition = "(" + self.condition + "AND " + other.build_condition() + ") "
        return and_condition

    def __or__(self, other):
        or_condition = DBCondition()
        or_condition.const=self.const + other.const
        or_condition.condition = "(" + self.condition + "OR " + other.build_condition() + ") "
        return or_condition


### u.enterprise_id = e.id
class ColumnCondition:
    def __init__(self, base_term: str, operator: SqlOperator, join_term: str):
        self.base_term = base_term
        self.operator = operator
        self.join_term = join_term

    def build_join_condition(self):
        self.condition = self.base_term + self.operator.column_operator + self.join_term
        return self.condition


class DBAssignment:
    def __init__(self, update_set: dict):
        self.update_set = update_set
        self.update_list = []
        self.value_list = []
        self.update_query = ""
    def build_assignment(self):
        for i, key_val in enumerate(self.update_set.items()):
            self.update_list.append(key_val[0] + '=' + "(${})")
            self.value_list.append(key_val[1])
        return self




# assign = DBAssignment({"username":"mahdi", "password":"7201172011"})
# assign = assign.build_assignment()
# print(assign)


# cd1 = DBUpdate(term='password',operator='=',const='mahdi')
# cd1.build_condition()
# cd2 = DBUpdate(term='userid',operator='=',const=5642)
# cd2.build_condition()
# cd3 = DBUpdate(term='userename',operator='=',const="mahdi")
# cd3.build_condition()
# final_update = cd1.__and__(cd2).__and__(cd3)
# print(final_update.condition)


# cd1 = DBCondition(term='password',operator='=',const='mahdi')
# cd1.build_condition()
# cd2 = DBCondition(term='userid',operator='=',const=5642)
# cd2.build_condition()
# cd3 = DBCondition('created_at','>',datetime.now())
# cd3.build_condition()
# cd4 = DBCondition('expire_at','>',datetime.now())
# cd4.build_condition()

# a = cd1.__or__(cd2).__and__(cd3).__or__(cd4)
# print(a.condition)
# print(a.const)



# print(cd1.condition)
# print(cd2.condition)
# print(cd2.const)


# const=5642
# const = [].append(const) #if type(const) is not list else [].extend(const)
# print(const)