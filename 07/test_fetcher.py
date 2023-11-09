import argparse
import os
import sys
import pytest
import asyncio
import fetcher
from unittest.mock import AsyncMock, Mock, patch

print_lock = asyncio.Lock()


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def file_content():
    content = (
        "https://stepik.org/course/128891/promo\n"
        "https://stepik.org/course/92012/promo"
    )
    with open('temp.txt', 'w', encoding='utf-8') as temp_file:
        temp_file.write(content)


def test_get_args():
    sys.argv = ["fetcher.py", '2', "urls.txt"]
    assert fetcher.get_args() == (2, 'urls.txt')

    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["fetcher.py", '2', "urls.tx"]
        fetcher.get_args()

    with pytest.raises(argparse.ArgumentError):
        sys.argv = ["fetcher.py", '0', "urls.tx"]
        fetcher.get_args()


def test_generator_url(file_content):
    PATH = "temp.txt"
    expected_answer = [
        "https://stepik.org/course/128891/promo",
        "https://stepik.org/course/92012/promo"
    ]
    assert list(fetcher.generator_url(PATH)) == expected_answer
    delete_file(PATH)


@pytest.mark.asyncio
@patch('fetcher.aiohttp.ClientSession.get')
def test_fetch_url_success(mock_response):
    url = ""
    counter = {"completed": 0}
    response = AsyncMock()
    response.status = 200
    mock_response.return_value.__aenter__.return_value = response
    asyncio.run(fetcher.fetch_url(url, counter, print_lock))
    assert counter["completed"] == 1
    mock_response.assert_called_once_with(url)


@pytest.mark.asyncio
@patch('fetcher.aiohttp.ClientSession.get')
def test_fetch_url_failure(mock_response):
    url = ""
    counter = {"completed": 0}
    response = AsyncMock()
    response.status = 0
    mock_response.return_value.__aenter__.return_value = response
    asyncio.run(fetcher.fetch_url(url, counter, print_lock))
    assert counter["completed"] == 0
    mock_response.assert_called_once_with("")
