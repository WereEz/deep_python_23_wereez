import argparse
import os
import sys
import asyncio
import unittest
from unittest.mock import AsyncMock, patch
import pytest
import fetcher


print_lock = asyncio.Lock()


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def file_content():
    content = (
        "1\n"
        "3\n"
        "2"
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


def test_generator_url():
    file_content()
    path = "temp.txt"
    expected_answer = [
        "1",
        "3",
        "2"
    ]
    assert list(fetcher.generator_url(path)) == expected_answer
    delete_file(path)


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


@pytest.mark.asyncio
async def test_fetch_several_urls():
    coroutines = 4
    file_path = "temp.txt"
    file_content()

    async def fake_fetch_url():
        await asyncio.sleep(0.1)

    with patch('fetcher.fetch_url', side_effect=fake_fetch_url) as mock_fetch_url:
        await fetcher.fetch_several_urls(coroutines, file_path)

    assert mock_fetch_url.call_count == 3
    called_args = set(i[0][0] for i in mock_fetch_url.call_args_list)
    expected_urls = {'3', '2', '1'}
    assert called_args == expected_urls
    delete_file(file_path)


@pytest.mark.asyncio
@patch('fetcher.aiohttp.ClientSession.get')
async def test_fetch_url_success_multiple(mock_response):
    urls = ["url1", "url2", "url3"]
    counter = {"completed": 0}
    responses = [AsyncMock(status=200) for _ in range(len(urls))]
    mock_response.side_effect = responses

    await asyncio.gather(*(fetcher.fetch_url(url, counter, print_lock) for url in urls))

    assert counter["completed"] == len(urls)
    expected_urls = [
        unittest.mock.call(url) for url in urls
    ]
    assert mock_response.call_args_list == expected_urls


@pytest.mark.asyncio
@patch('fetcher.aiohttp.ClientSession.get')
async def test_fetch_url_failure_multiple(mock_response):
    urls = ["url1", "url2", "url3"]
    counter = {"completed": 0}
    response = AsyncMock()
    response.status = 0
    mock_response.return_value.__aenter__.return_value = response

    await asyncio.gather(*(fetcher.fetch_url(url, counter, print_lock) for url in urls))

    assert counter["completed"] == 0
    expected_urls = [
        unittest.mock.call(url) for url in urls
    ]
    assert mock_response.call_args_list == expected_urls
