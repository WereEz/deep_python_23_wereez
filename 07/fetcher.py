import os
import time
import asyncio
import argparse
import aiohttp


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('coroutines', type=int,
                        help='Количество одновременных запросов')
    parser.add_argument('file_urls', type=str, help='Файл с урлами')
    args = parser.parse_args()
    if args.coroutines <= 0:
        raise argparse.ArgumentError(
            None, "Количество одновременных запросов должно быть больше 0")
    if not os.path.exists(args.file_urls):
        raise argparse.ArgumentError(None, "Неправильный путь к файлу")
    return args.coroutines, args.file_urls


def generator_url(path):
    with open(path, 'r', encoding='utf-8') as file:
        for url in file:
            yield url.strip()


async def fetch_url(url, counter, print_lock):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status:
                async with print_lock:
                    counter['completed'] += 1
                    print(f"{counter['completed']}: {url}")


async def fetch_worker(que, counter, print_lock):
    while True:
        url = await que.get()
        try:
            await fetch_url(url, counter, print_lock)
        finally:
            que.task_done()


async def fetch_several_urls(nums_coroutines, path):
    t_1 = time.time()
    que = asyncio.Queue()
    counter = {'completed': 0}
    print_lock = asyncio.Lock()
    workers = [
        asyncio.create_task(fetch_worker(que, counter, print_lock))
        for _ in range(nums_coroutines)
    ]
    for url in generator_url(path):
        await que.put(url)
    await que.join()
    for worker in workers:
        worker.cancel()
    t_2 = time.time()
    print(t_2 - t_1)

if __name__ == "__main__":
    coroutines, file_path = get_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_several_urls(coroutines, file_path))
