import time
import pytest
from unittest import mock
from json_parser import parse_json, mean


@pytest.fixture
def mock_callback():
    return mock.Mock()


@pytest.fixture
def mock_json_data():
    return '{"key1": "Word1 word2", "key2": "word2 word3"}'


def test_parse_json_how_much_callback(mock_json_data, mock_callback):
    json_str = mock_json_data
    required_fields = ["key1", "key2"]
    keywords = ["word2"]
    expected_result = 2
    keyword_callback = mock_callback.callback
    parse_json(json_str, required_fields, keywords, keyword_callback)
    assert len(keyword_callback.mock_calls) == expected_result


def test_parse_json_case_sensitive_required_fields(mock_json_data,
                                                   mock_callback):
    json_str = mock_json_data
    required_fields = ["KeY1"]
    keywords = ["word2"]
    expected_calls = []
    keyword_callback = mock_callback.callback
    parse_json(json_str, required_fields, keywords, keyword_callback)
    assert expected_calls == mock_callback.mock_calls


def test_parse_json_not_case_sensitive_keyword(mock_json_data,
                                               mock_callback):
    json_str = mock_json_data
    required_fields = ["key1"]
    keywords = ["wOrD2"]
    keyword_callback = mock_callback.callback
    expected_calls = [mock.call.callback("word2")]
    parse_json(json_str, required_fields, keywords, keyword_callback)
    assert expected_calls == mock_callback.mock_calls


def test_parse_json_two_different_words_in_one_required_fields(
        mock_json_data, mock_callback):
    json_str = mock_json_data
    required_fields = ["key2"]
    keywords = ["word2", "word3"]
    keyword_callback = mock_callback.callback

    expected_calls = [mock.call.callback('word2'), mock.call.callback('word3')]

    parse_json(json_str, required_fields, keywords, keyword_callback)
    assert expected_calls == mock_callback.mock_calls


def test_parse_json_word_twice_in_one_line(mock_json_data, mock_callback):
    json_str = '{"key1": "Ёж ёж", "key2": "word2 word3"}'
    required_fields = ["key1"]
    keywords = ["ёж"]
    keyword_callback = mock_callback.callback

    expected_calls = [mock.call.callback('ёж'), mock.call.callback('ёж')]

    parse_json(json_str, required_fields, keywords, keyword_callback)
    assert expected_calls == mock_callback.mock_calls


def test_mean_decorator():
    @mean(5)  # Усреднять последние 5 вызовов
    def slow_function(duration):
        time.sleep(duration)
    with mock.patch('builtins.print') as mock_print:
        slow_function(0.1)
        slow_function(0.2)
        slow_function(0.3)
        slow_function(0.4)
        slow_function(0.5)
        expected_ans = 0.3
        mean_time = float(mock_print.call_args_list[-1][0][0].split()[-2])
        assert abs(mean_time - expected_ans) < 0.05


if __name__ == "__main__":
    pytest.main()
