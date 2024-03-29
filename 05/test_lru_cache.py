import pytest
from lru_cache import LRUCache

def test_as_in_task():
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"
    cache.set("k3", "val3")
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"

def test_incorrect_limit():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(TypeError):
        LRUCache("41")
    new_cache = LRUCache(2)
    assert new_cache.limit == 2


def test_change_value():
    new_cache = LRUCache(2)
    new_cache.set("k1", "1")
    assert new_cache.get("k1") == "1"
    new_cache.set("k2", "2")
    assert new_cache.get("k2") == "2"
    new_cache.set("k1", "hedgegog")
    assert new_cache.get("k1") == "hedgegog"


def test_eviction_of_old_values():
    small_cache = LRUCache(2)
    small_cache.set("k1", "1")
    small_cache.set("k2", "2")
    assert len(small_cache.dct) == 2
    small_cache.set("k3", "3")
    assert small_cache.get("k1") is None
    assert small_cache.get("k2") == "2"
    assert small_cache.get("k3") == "3"
    small_cache.get("k2")
    small_cache.set("k4", "4")
    assert small_cache.get("k3") is None
    assert small_cache.get("k2") == "2"
    assert small_cache.get("k4") == "4"
    assert len(small_cache.dct) == 2

def test_with_limig_one():
    small_cache = LRUCache(1)
    small_cache.set("k1", "1")
    assert small_cache.get("k1") == "1"
    assert len(small_cache.dct) == 1
    small_cache.set("k2", "2")
    assert len(small_cache.dct) == 1
    assert small_cache.get("k1") is None
    assert small_cache.get("k2") == "2"

def test_pop_not_change():
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    assert cache.get("k1") == "val1"
    assert cache.get("k2") == "val2"
    cache.set("k1", "1")
    cache.set("k3", "val3")
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "1"