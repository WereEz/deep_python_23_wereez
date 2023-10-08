"""Модуль с кодом json парсера и декоратора
среднего времени последних K вызовов"""
import time
import json


def parse_json(json_str: str, required_fields=None,
               keywords=None, keyword_callback=None):
    """Принимает строку, в которой содержится json,
        и производит парсинг этого json"""
    if required_fields is None or keywords is None or keyword_callback is None:
        return
    parsed_json = json.loads(json_str)
    keywords = [key.lower() for key in keywords]
    for (key, value) in parsed_json.items():
        if key in required_fields:
            for word in value.lower().split(" "):
                if word in keywords:
                    keyword_callback(key, word)


def mean(k):
    """Декоратор среднего времени последних K вызовов"""
    def decorator(func):
        timings = []

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            timings.append(end_time - start_time)
            if len(timings) > k:
                timings.pop(0)
            avg_time = sum(timings) / len(timings)
            print(
                f"Среднее время последних {k} вызовов: {avg_time:.3f} секунд")
            return result
        return wrapper
    return decorator
