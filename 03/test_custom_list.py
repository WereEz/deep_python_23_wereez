from custom_list import CustomList


def assert_custom_list_equal(custom_list1, custom_list2):
    assert custom_list1 == custom_list2
    assert list(custom_list1) == list(custom_list2)


def test_custom_list_add():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([1, 2, 7])
    result1 = custom_list1 + custom_list2
    assert_custom_list_equal(result1, CustomList([6, 3, 10, 7]))
    # Проверяем, что исходный список не изменился
    assert_custom_list_equal(custom_list1, CustomList([5, 1, 3, 7]))
    assert_custom_list_equal(custom_list2, CustomList([1, 2, 7]))
    result2 = custom_list1 + [2, 5]
    assert_custom_list_equal(result2, CustomList([7, 6, 3, 7]))
    result3 = custom_list2 + [1, 2, 3, 4]
    assert_custom_list_equal(result3, CustomList([2, 4, 10, 4]))


def test_custom_list_add_empty():
    custom_list1 = CustomList([])
    result1 = custom_list1 + [1]
    assert_custom_list_equal(result1, CustomList([1]))
    result2 = [1] + custom_list1
    assert_custom_list_equal(result2, CustomList([1]))
    result3 = [] + custom_list1
    assert_custom_list_equal(result3, CustomList([]))


def test_custom_list_radd():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([1, 2, 7])
    result1 = [2, 5] + custom_list1
    assert_custom_list_equal(result1, CustomList([7, 6, 3, 7]))
    # Проверяем, что исходный список не изменился
    assert_custom_list_equal(custom_list1, CustomList([5, 1, 3, 7]))
    assert_custom_list_equal(custom_list2, CustomList([1, 2, 7]))
    result2 = custom_list2 + [1, 2, 3, 4]
    assert_custom_list_equal(result2, CustomList([2, 4, 10, 4]))


def test_custom_list_sub():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([1, 2, 7])
    result1 = custom_list1 - custom_list2
    assert_custom_list_equal(result1, CustomList([4, -1, -4, 7]))
    # Проверяем, что исходный список не изменился
    assert_custom_list_equal(custom_list1, CustomList([5, 1, 3, 7]))
    assert_custom_list_equal(custom_list2, CustomList([1, 2, 7]))
    result2 = custom_list1 - [1, 2, 7]
    assert_custom_list_equal(result2, CustomList([4, -1, -4, 7]))
    result3 = custom_list2 - [1, 2, 3, 4]
    assert_custom_list_equal(result3, CustomList([0, 0, 4, -4]))


def test_custom_list_sub_empty():
    custom_list1 = CustomList([])
    result1 = custom_list1 - [1]
    assert_custom_list_equal(result1, CustomList([-1]))
    result2 = [1] - custom_list1
    assert_custom_list_equal(result2, CustomList([1]))
    result3 = [] - custom_list1
    assert_custom_list_equal(result3, CustomList([]))


def test_custom_list_rsub():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([1, 2, 7])
    result1 = [1, 2, 7] - custom_list1
    assert_custom_list_equal(result1, CustomList([-4, 1, 4, -7]))
    # Проверяем, что исходный список не изменился
    assert_custom_list_equal(custom_list1, CustomList([5, 1, 3, 7]))
    assert_custom_list_equal(custom_list2, CustomList([1, 2, 7]))
    result2 = [1, 2, 3, 4] - custom_list2
    assert_custom_list_equal(result2, CustomList([0, 0, -4, 4]))


def test_custom_list_comparison():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([1, 2, 7])
    custom_list3 = CustomList([5, 1, 3, 7])

    assert custom_list1 == custom_list3
    assert custom_list1 != custom_list2
    assert custom_list1 > custom_list2
    assert custom_list2 < custom_list1
    assert custom_list1 >= custom_list3
    assert custom_list1 <= custom_list3


def test_lists_with_same_sum():
    custom_list1 = CustomList([3, 5, 2])
    custom_list2 = CustomList([1, 4, 5])
    assert custom_list1 == custom_list2
    assert (custom_list1 != custom_list2) is False
    assert (custom_list1 > custom_list2) is False
    assert (custom_list1 < custom_list2) is False
    assert custom_list1 >= custom_list2
    assert custom_list1 <= custom_list2


def test_custom_list_and_not_custom_listcomparison():
    custom_list1 = CustomList([5, 1, 3, 7])
    assert (custom_list1 == [5, 1, 3, 7]) is None
    assert (custom_list1 != [5, 1, 3, 7]) is None
    assert (custom_list1 > [5, 1, 3, 7]) is None
    assert (custom_list1 < [5, 1, 3, 7]) is None
    assert (custom_list1 >= [5, 1, 3, 7]) is None
    assert (custom_list1 <= [5, 1, 3, 7]) is None


def test_str():
    custom_list1 = CustomList([5, 1, 3, 7])
    custom_list2 = CustomList([])
    assert str(custom_list1) == "[5, 1, 3, 7] Сумма = 16"
    assert str(custom_list2) == "[] Сумма = 0"
