import pytest
from lru_cache import LRUCache


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
