import cProfile
import pstats
from functools import wraps


def profile_deco(func):
    profiler = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = profiler.runcall(func, *args, **kwargs)
        return result

    def print_stat():
        stats = pstats.Stats(profiler)
        print(f"Для функции - {func.__name__}")
        stats.sort_stats("cumulative").print_stats()

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


def main():
    add(4, 5)
    add(1, 2)
    sub(4, 5)

    for i in range(500_000):
        add(i, i)
        sub(i, i)

    add.print_stat()
    sub.print_stat()


if __name__ == "__main__":
    main()
