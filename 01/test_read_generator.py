import os
import pytest
from read_generator import search_words_in_file


@pytest.fixture
def file_content_one_line():
    content_one_line = (
        "кактусовый"
    )
    with open('temp.txt', 'w', encoding='utf-8') as temp_file:
        temp_file.write(content_one_line)

    # Открываем созданный файл и возвращаем его как объект TextIOWrapper
    return open('temp.txt', 'r', encoding='utf-8')


@pytest.fixture
def file_content():
    content = (
        "Ехал Грека через реку\n"
        "видит Грека в реке\n"
        "Сунул Грека руку в реку\n"
        "рак за руку Греку - цап!\n"
        "Ёжик"
    )
    with open('temp.txt', 'w', encoding='utf-8') as temp_file:
        temp_file.write(content)

    # Открываем созданный файл и возвращаем его как объект TextIOWrapper
    return open('temp.txt', 'r', encoding='utf-8')


@pytest.fixture
def file_name(tmp_path):
    # Создаем временный файл и записываем в него текст
    file_path = tmp_path / "test_file.txt"
    content = (
        "Ехал Грека через реку\n"
        "видит Грека в реке\n"
        "Сунул Грека руку в реку\n"
        "рак за руку Греку - цап!\n"
        "Ёжик"
    )
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return str(file_path)


def delete_file(file):
    # Получаем путь к файлу из файлового объекта
    file_path = file.name

    # Удаляем файл, если он существует
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def words():
    return ["Грека", "Ёжик", "рак"]


@pytest.fixture
def expected_answer():
    return [
        "Ехал Грека через реку",
        "видит Грека в реке",
        "Сунул Грека руку в реку",
        "рак за руку Греку - цап!",
        "Ёжик",
    ]


def test_read_generator_with_file_one_word(file_name):
    words = ["Ёжик"]
    expected_result = ["Ёжик"]
    result = list(search_words_in_file(file_name, words))
    assert result == expected_result


def test_read_generator_nothing_found(file_name):
    words = ["hedgehog"]
    result = list(search_words_in_file(file_name, words))
    assert result == []


def test_read_generator_with_io_file(file_content, words, expected_answer):
    result = list(search_words_in_file(file_content, words))
    assert result == expected_answer
    delete_file(file_content)


def test_read_generator_incorrect_input():
    with pytest.raises(ValueError):
        list(search_words_in_file(5, []))

    with pytest.raises(ValueError):
        list(search_words_in_file(["some list"], []))


def test_read_generator_case_insensitive(file_name):
    words = ["ёжик"]
    expected_result = [
        "Ёжик",
    ]
    result = list(search_words_in_file(file_name, words))
    assert result == expected_result


def test_read_generator_multiple_words_in_line(file_name):
    words = ["рак", "руку"]
    expected_result = [
        "Сунул Грека руку в реку",
        "рак за руку Греку - цап!",
    ]
    result = list(search_words_in_file(file_name, words))
    assert result == expected_result


def test_read_generator_partial_word_match(file_content_one_line):
    words = ["кактус"]
    result = list(search_words_in_file(file_content_one_line, words))
    assert result == []
    delete_file(file_content_one_line)


def test_read_generator_whole_word_match_in_file(
        file_content_one_line):
    words = ["кактусовый"]
    expected_result = ["кактусовый"]
    result = list(search_words_in_file(file_content_one_line, words))
    assert result == expected_result
    delete_file(file_content_one_line)
