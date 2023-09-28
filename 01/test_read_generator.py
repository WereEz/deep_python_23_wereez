import io
import pytest
from read_generator import search_words_in_file


@pytest.fixture
def file_content():
    content = (
        "Ехал Грека через реку\n"
        "видит Грека в реке\n"
        "Сунул Грека руку в реку\n"
        "рак за руку Греку - цап!\n"
        "Ёж"
    )
    return io.StringIO(content)


@pytest.fixture
def file_name(tmp_path):
    # Создаем временный файл и записываем в него текст
    file_path = tmp_path / "test_file.txt"
    content = (
        "Ехал Грека через реку\n"
        "видит Грека в реке\n"
        "Сунул Грека руку в реку\n"
        "рак за руку Греку - цап!\n"
        "Ёж"
    )
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return str(file_path)


@pytest.fixture
def words():
    return ["Грека", "Ёж", " ", "рек", "реку"]


@pytest.fixture
def expected_answer():
    return [
        "Ехал Грека через реку",
        "видит Грека в реке",
        "Сунул Грека руку в реку",
        "рак за руку Греку - цап!",
        "Ёж",
    ]


def test_read_generator_with_file_one_word(file_name):
    words = ["Ёж"]
    expected_result = ["Ёж"]
    result = list(search_words_in_file(file_name, words))
    assert result == expected_result


def test_read_generator_nothing_found(file_name):
    words = ["hedgehog"]
    result = list(search_words_in_file(file_name, words))
    assert result == []


def test_read_generator_with_io_file(file_content, words, expected_answer):
    result = list(search_words_in_file(file_content, words))
    assert result == expected_answer


def test_read_generator_incorrect_input():
    with pytest.raises(ValueError):
        list(search_words_in_file(5, []))

    with pytest.raises(ValueError):
        list(search_words_in_file(["some list"], []))
