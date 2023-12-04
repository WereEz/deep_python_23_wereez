import json
import ujson
import cjson
import pytest


@pytest.fixture
def sample_dict():
    return {
        "name": "John Doe",
        "age": 25,
        "city": "JSON city",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }


def test_loads(sample_dict):
    json_str = '{"hello": 10, "world": "value"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    assert json_doc == ujson_doc == cjson_doc

    cjson_result = cjson.dumps(sample_dict)
    json_result = json.dumps(sample_dict)
    assert cjson_result == json_result


def test_dumps(sample_dict):
    json_str = '{"hello": 10, "world": "value"}'
    assert json_str == cjson.dumps(cjson.loads(json_str))

    cjson_result = cjson.dumps(sample_dict)
    json_result = json.dumps(sample_dict)
    assert cjson_result == json_result


if __name__ == "__main__":
    pytest.main()
