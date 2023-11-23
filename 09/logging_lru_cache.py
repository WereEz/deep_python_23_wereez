import argparse
import logging


class CustomFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        if len(message) % 2 == 0:
            return False
        return True


def set_logger(flag_stdout, flag_filter):
    format_sentry = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t[stdout]\t%(message)s"
    )
    format_example = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t[file]\t%(message)s"
    )

    fake_sentry = logging.StreamHandler()
    fake_sentry.setLevel(logging.INFO)
    fake_sentry.setFormatter(format_sentry)

    default_log = logging.FileHandler("cache.log", encoding='utf-8')
    default_log.setLevel(logging.INFO)
    default_log.setFormatter(format_example)

    full = logging.getLogger("full")
    full.setLevel(logging.INFO)
    full.addHandler(default_log)
    if flag_filter:
        full.addFilter(CustomFilter())
    if flag_stdout:
        full.addHandler(fake_sentry)
    return logging.getLogger("full")


class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError
        if limit <= 0:
            raise ValueError
        self.limit = limit
        self.dct = {}

    def get(self, key):
        if key not in self.dct:
            logger.warning('Получен не существующий ключ: %s', key)
            return None
        self.dct[key] = self.dct.pop(key)
        logger.info('Получен существующий ключ: %s: %s', key, self.dct[key])
        return self.dct[key]

    def set(self, key, value):
        if key in self.dct:
            logger.info(
                'Удаление ключа: %s. Причина: переместить ключ после вызова',
                key)
            self.dct.pop(key)
        if self.limit == len(self.dct):
            logger.info('Удаление ключа: %s. Причина: предел по ёмкости', key)
            self.dct.pop(next(iter(self.dct)))
        logger.info('Установка ключа %s: %s', key, value)
        self.dct[key] = value


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stdout', action='store_true',
                        help='Логгирование в поток стандартного вывода')
    parser.add_argument('-f', '--filter', action='store_true',
                        help='Отбрасываем записи с четным числом символов')
    args = parser.parse_args()
    return args.stdout, args.filter


def main():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    cache.get("k3")
    cache.get("k2")
    cache.get("k1")
    cache.set("k1", "val2")
    cache.set("k3", "val3")

    cache.get("k3")
    cache.get("k2")
    cache.get("k1")


if __name__ == "__main__":
    stdo, filt = get_args()
    logger = set_logger(stdo, filt)
    main()
