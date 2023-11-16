import cProfile
import pstats
import weakref
from memory_profiler import profile

class MyInteger:
    def __init__(self, value):
        self.value = value

class NormalClass:
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    @property
    def attr1(self):
        return self._attr1

    @property
    def attr2(self):
        return self._attr2

class SlottedClass:
    __slots__ = ['_attr1', '_attr2']
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    @property
    def attr1(self):
        return self._attr1

    @property
    def attr2(self):
        return self._attr2

class WeakRefClass:
    def __init__(self, attr1, attr2):
        self._attr1 = weakref.ref(attr1)
        self._attr2 = weakref.ref(attr2)

    @property
    def attr1(self):
        return self._attr1()

    @property
    def attr2(self):
        return self._attr2()

def create_instances_normal_class_for_time(number=100000):
    print("Обычный класс")
    prof = cProfile.Profile()
    prof.enable()
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(NormalClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1
    prof.disable()
    stat = pstats.Stats(prof).sort_stats("cumulative")
    stat.print_stats()

def create_instances_slotted_class_for_time(number=100000):
    print("Класс со слотами")
    prof = cProfile.Profile()
    prof.enable()
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(SlottedClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1
    prof.disable()
    stat = pstats.Stats(prof).sort_stats("cumulative")
    stat.print_stats()


def create_instances_weakref_class_for_time(number=100000):
    print("Класс со слабыми ссылками")
    prof = cProfile.Profile()
    prof.enable()
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(WeakRefClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1
    prof.disable()
    stat = pstats.Stats(prof).sort_stats("cumulative")
    stat.print_stats()

@profile
def create_instances_normal_class_for_memory(number=100000):
    print("Обычный класс")
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(NormalClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1

@profile
def create_instances_slotted_class_for_memory(number=100000):
    print("Класс со слотами")
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(SlottedClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1

@profile
def create_instances_weakref_class_for_memory(number=100000):
    print("Класс со слабыми ссылками")
    attr1 = MyInteger(1)
    attr2 = MyInteger(2)
    instances = []
    for _ in range(number):
        instances.append(WeakRefClass(attr1,attr2))
    for item in instances:
        item.attr1.value += 1

def main():
    NUMBER = 1000000
    # create_instances_normal_class_for_time(NUMBER)
    # create_instances_slotted_class_for_time(NUMBER)
    # create_instances_weakref_class_for_time(NUMBER)
    create_instances_normal_class_for_memory(NUMBER)
    create_instances_slotted_class_for_memory(NUMBER)
    create_instances_weakref_class_for_memory(NUMBER)

if __name__ == "__main__":
    main()
    

