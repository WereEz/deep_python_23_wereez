"""Тестирование модуля func_predict"""
from unittest import mock
import pytest
from func_predict import SomeModel, predict_message_mood


@pytest.fixture
def test_model():
    return SomeModel()


@pytest.fixture
def mock_model():
    return mock.Mock(spec=SomeModel)


def test_predict_model(test_model, mock_model):
    with mock.patch("func_predict.SomeModel.predict") as mock_predict:
        mock_predict.return_value = 1/3
        assert test_model.predict("1/3") == 1/3
        assert [mock.call("1/3")] == mock_predict.mock_calls

        mock_predict.return_value = 1000
        assert test_model.predict("1000") == 1000.0
        expected_calls = [mock.call("1/3"), mock.call("1000")]
        assert expected_calls == mock_predict.mock_calls


def test_what_is_passed_to_predict_model(test_model, mock_model):
    with mock.patch("func_predict.SomeModel.predict") as mock_predict:
        test_model.predict("1/3")
        assert [mock.call("1/3")] == mock_predict.mock_calls
        test_model.predict("1000")
        expected_calls = [mock.call("1/3"), mock.call("1000")]
        assert expected_calls == mock_predict.mock_calls


def test_predict_message_mood(test_model):
    assert predict_message_mood("", test_model) == "норм"
    assert predict_message_mood("", test_model, 0.1, 0.1) == "отл"
    assert predict_message_mood("", test_model, 100) == "неуд"
    assert predict_message_mood("", test_model, 0.5, 0.5) == "норм"


def test_model_change_thresholds_predict(mock_model):
    mock_model.predict.return_value = 5
    assert predict_message_mood("", mock_model, 0, 4.99) == "отл"
    assert predict_message_mood("", mock_model, 0, 5.01) == "норм"
    assert predict_message_mood("", mock_model, 5.01, 10) == "неуд"


def test_model_predict_thresholds(mock_model):
    # Проверяем, что пороговые значения правильно обрабатываются
    mock_model.predict.return_value = 4.99
    lower_threshold = 0
    upper_threshold = 4.99
    assert predict_message_mood(
        "", mock_model, lower_threshold, upper_threshold) == "норм"
    mock_model.predict.return_value = 0
    assert predict_message_mood(
        "", mock_model, lower_threshold, upper_threshold) == "норм"

    # Проверяем, что значения около порогов обрабатываются корректно
    mock_model.predict.return_value = 4.98001
    lower_threshold = 4.98
    upper_threshold = 5.01
    assert predict_message_mood(
        "", mock_model, lower_threshold, upper_threshold) == "норм"
    mock_model.predict.return_value = 5.0100001
    assert predict_message_mood(
        "", mock_model, lower_threshold, upper_threshold) == "отл"
