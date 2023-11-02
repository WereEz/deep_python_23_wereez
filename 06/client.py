import concurrent.futures
import argparse
import json
import socket
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('threads', type=int, help='Количество потоков')
    parser.add_argument('file_urls', type=str, help='Файл с урлами')
    args = parser.parse_args()
    if args.threads <= 0:
        raise argparse.ArgumentError(None, "Потоков должно быть больше 0")
    if not os.path.exists(args.file_urls):
        raise argparse.ArgumentError(None, "Неправильный путь к файлу")
    return args.threads, args.file_urls


def start_client(file_path, num_threads):
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(num_threads) as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(send_request, url))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def send_request(url):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soct:
        soct.connect(("localhost", 8888))
        soct.sendall(url.encode())
        data = soct.recv(1024)
    return f"{url}: {json.loads(data.decode())}"


def main():
    threads, file_url = get_args()
    start_client(file_url, threads)


if __name__ == '__main__':
    main()
