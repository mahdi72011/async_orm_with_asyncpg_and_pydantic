from datetime import datetime



class DBCondition:
    def __init__(self, term: str=None, operator: str=None, const: object=None, starting_index: int=1):
        self.term = term
        self.operator = operator
        self.condition = ""
        self.number = starting_index
        self.const = (list(const),) if isinstance(const, (list, tuple)) else (const,)

    def build_condition(self):
        self.condition = self.term + self.operator + f"(${self.number}) "
        return self.condition

    def __and__(self, other):
        other.number += self.number
        and_condition = DBCondition(const=self.const + other.const)
        and_condition.number = other.number
        and_condition.condition = "(" + self.condition + "AND " + other.build_condition() + ") "
        return and_condition

    def __or__(self, other):
        other.number += self.number
        or_condition = DBCondition(const=self.const + other.const)
        or_condition.number = other.number
        or_condition.condition = "(" + self.condition + "OR " + other.build_condition() + ") "
        return or_condition

class DBAssignment:
    def __init__(self, update_set: dict):
        self.update_set = update_set
        self.update_list = []
        self.value_list = []
    def build_assignment(self):
        for i, key_val in enumerate(self.update_set.items()):
            self.update_list.append(key_val[0] + '=' + f"(${i+1})")
            self.value_list.append(key_val[1])
        return self.update_list, self.value_list




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



# def update(update: list, update_constant: list, condition: str=None, condition_constant: list=None):
#     query = "UPDATE {table} SET {update} WHERE {condition};". \
#         format(table="orders",
#                 update=",".join(update),
#                 condition=condition)
#     return query

# c = DBCondition(term="orderid", operator="=", const=12, starting_index=2)
# c.build_condition()

# up = DBAssignment({"is_paid": True})
# up.build_assignment()

# a = update(update=up.update_list, update_constant=up.value_list, condition=c.condition, condition_constant=c.const)

# print(a)


