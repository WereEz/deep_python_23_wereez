class Integer:
    def __get__(self, obj, objtype):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        return setattr(obj, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"int_descr_{name}"


class String:
    def __get__(self, obj, objtype):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        setattr(obj, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"str_descr_{name}"


class PositiveInteger:
    def __get__(self, obj, objtype):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Value must be a positive integer")
        setattr(obj, self.name, value)

    def __set_name__(self, owner, name):
        self.name = f"posit_int_descr_{name}"


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
