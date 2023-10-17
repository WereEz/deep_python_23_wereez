import pytest
from meta import CustomClass


def test_class():
    assert CustomClass.custom_x == 50
    with pytest.raises(AttributeError):
        assert CustomClass.x


def test_instance():
    inst = CustomClass()
    assert inst.custom_x == 50
    assert inst.custom_val == 99
    assert inst.custom_line() == 100
    assert str(inst) == "Custom_by_metaclass"
    with pytest.raises(AttributeError):
        assert inst.x
    with pytest.raises(AttributeError):
        assert inst.line()


def test_added_attributes_instance():
    inst = CustomClass()
    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"
    with pytest.raises(AttributeError):
        assert inst.dynamic


def test_invalid_value():
    inst = CustomClass()

    assert inst.custom_x == 50
    inst.custom_x = 5000
    assert inst.custom_x == 50
    assert inst.custom_custom_x == 5000

    assert inst.custom_line() == 100
    inst.custom_line = lambda: 5000
    assert inst.custom_line() == 100
    assert inst.custom_custom_line() == 5000

    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"
    inst.dynamic = "some changes"
    assert inst.custom_dynamic == "added later"
