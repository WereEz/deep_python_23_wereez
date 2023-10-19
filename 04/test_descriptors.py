import pytest
from descriptors import Data


@pytest.fixture
def test_data():
    return Data(10, 'example', 100)


def test_integer_descriptor(test_data):
    assert test_data.num == 10
    test_data.num = -10
    assert test_data.num == -10
    with pytest.raises(ValueError):
        test_data.num = 'string'
    with pytest.raises(ValueError):
        test_data.num = 1.5


def test_string_descriptor(test_data):
    assert test_data.name == 'example'
    test_data.name = "hedgehog"
    assert test_data.name == "hedgehog"
    with pytest.raises(ValueError):
        test_data.name = 123


def test_positive_integer_descriptor(test_data):
    assert test_data.price == 100
    test_data.price = 0
    assert test_data.price == 0
    with pytest.raises(ValueError):
        test_data.price = 'string'
    with pytest.raises(ValueError):
        test_data.price = -50


def test_invalid_value(test_data):
    assert test_data.num == 10
    with pytest.raises(ValueError):
        test_data.num = "asidja"
    assert test_data.num == 10
    assert test_data.name == 'example'
    with pytest.raises(ValueError):
        test_data.name = 123
    assert test_data.name == "example"
    assert test_data.price == 100
    with pytest.raises(ValueError):
        test_data.price = -1
    assert test_data.price == 100
