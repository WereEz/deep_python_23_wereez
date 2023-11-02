import argparse
import json
import threading
import server
import socket
import sys
import pytest
import client
import warnings
from unittest import mock


def test_client_get_args_valid_input():
    sys.argv = ["client.py", '2', "urls.txt"]
    assert client.get_args() == (2, 'urls.txt')


def test_client_get_args_invalid_threads():
    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["client.py", '2', "urls.tx"]
        client.get_args()


def test_client_get_args_invalid_file_path():
    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["client.py", '-1', "urls.txt"]
        client.get_args()


def test_server_get_args_valid_input():
    sys.argv = ["server.py", '-w 2', '-k 3']
    assert server.get_args() == (2, 3)


def test_server_get_args_invalid_workers():
    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["server.py", '-w -1', "-k 1"]
        server.get_args()


def test_server_get_args_invalid_top():
    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["server.py", '-w 1', "-k 0"]
        server.get_args()


def test_send_request():
    url = "http://example.com"
    with mock.patch('socket.socket') as mock_socket:
        mock_instance = mock_socket.return_value
        data = b'{"word": 5}'
        mock_instance.recv.return_value = data
        assert client.send_request(url) == data


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)
    server_socket.settimeout(1)
    client_socket, _ = server_socket.accept()
    while True:
        try:
            client_socket.send(json.dumps(
                {"test": 123, "foo": "bar"}).encode())
        except socket.timeout:
            break
    client_socket.close()
    server_socket.close()


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_send_request():
    threading.Thread(target=start_server).start()
    url = 'http://testurl.com'
    result = client.send_request(url)
    expected_result = f"{url}: {{'test': 123, 'foo': 'bar'}}"
    assert result == expected_result


def test_find_top_word():
    text = "This is Is a a this is"
    top = 3
    expected_result = {'is': 3, 'a': 2, 'this': 2}
    assert server.find_top_word(text, top) == expected_result
