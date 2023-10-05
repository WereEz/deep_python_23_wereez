"""Модуль с генератор для чтения и поиска по файлу"""
import io


def search_words_in_file(file, search_words):
    """Генератор для чтения и поиска по файлу"""
    if isinstance(file, (io.StringIO, str)):
        if isinstance(file, str):
            file = open(file, "r", encoding="utf-8")
        file.seek(0)
        for line in file:
            if any(word.lower() in line.lower().split()
                   for word in search_words):
                yield line.strip()
        file.close()
    else:
        raise ValueError()
