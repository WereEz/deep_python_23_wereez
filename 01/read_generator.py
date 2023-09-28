"""Модуль с генератор для чтения и поиска по файлу"""
import io


def search_words_in_file(file, search_words):
    """Генератор для чтения и поиска по файлу"""
    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as text:
            for line in text:
                if any(word.lower() in line.lower() for word in search_words):
                    yield line
    elif isinstance(file, io.StringIO):
        file.seek(0)
        for line in file:
            if any(word.lower() in line.lower() for word in search_words):
                yield line.strip()
    else:
        raise ValueError()
