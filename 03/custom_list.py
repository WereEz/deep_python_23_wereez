class CustomList(list):
    def __add__(self, other):
        len_self, len_other = len(self), len(other)
        min_len = min(len_self, len_other)
        result = CustomList([self[i] + other[i] for i in range(min_len)])
        result.extend(self[min_len:len_self])
        result.extend(other[min_len:len_other])
        return result

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        len_self, len_other = len(self), len(other)
        min_len = min(len_self, len_other)
        result = CustomList([self[i] - other[i] for i in range(min_len)])
        result.extend(self[min_len:len_self])
        result.extend([-other[i] for i in range(min_len, len_other)])
        return result

    def __rsub__(self, other):
        return CustomList([-x for x in self]) + other

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        return None

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        return None

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        return None

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        return None

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        return None

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        return None

    def __str__(self):
        return f"{super().__str__()} Сумма = {sum(self)}"
