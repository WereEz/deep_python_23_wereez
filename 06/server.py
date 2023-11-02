from collections import Counter
import concurrent.futures
import argparse
import json
import socket
import threading
from bs4 import BeautifulSoup

import requests


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', "--workers", type=int,
                        help='Количество воркеров')
    parser.add_argument('-k', '--top', type=int,
                        help='Количество самых популярных слов')
    args = parser.parse_args()
    if args.workers <= 0:
        raise argparse.ArgumentError(None, "Воркеров должно быть больше 0")
    if args.top <= 0:
        raise argparse.ArgumentError(None, "Число слов должно быть больше 0")
    return args.workers, args.top


def find_top_word(text, top):
    words = text.lower().split()
    word_counts = Counter(words)
    words_frequency = dict(word_counts.most_common(top))
    return words_frequency


def start_master(num_workers, nums_word):

    processed_urls = 0
    lock = threading.Lock()

    def handle_worker(client_socket, nums_word):
        nonlocal processed_urls
        url = client_socket.recv(1024).decode()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        words_frequency = find_top_word(soup.text, nums_word)
        response = json.dumps(words_frequency)
        client_socket.send(response.encode())
        with lock:
            processed_urls += 1
            print(f"Processed URLs: {processed_urls}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
        master_socket.bind(("localhost", 8888))
        master_socket.listen()
        master_socket.settimeout(10)
        with concurrent.futures.ThreadPoolExecutor(num_workers) as executor:
            while True:
                try:
                    client_socket, _ = master_socket.accept()
                    executor.submit(handle_worker, client_socket, nums_word)
                except socket.timeout:
                    print("Запросов не было 10 секунд отключаемся")
                    break


def main():
    workers, nums_word = get_args()
    print('server запущен')
    start_master(workers, nums_word)


if __name__ == "__main__":
    main()
