"""Tests for GET /rabbit/{n}."""
import os

import pytest
import requests

from conftest import BASE_URL
API_KEY = "aaa"
AUTH = {"X-API-Key": API_KEY}

# Known values: rabbit(n) follows the sequence 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
KNOWN_VALUES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 5),
    (5, 8),
    (6, 13),
    (7, 21),
    (8, 34),
    (9, 55),
    (10, 89),
]


@pytest.mark.parametrize("n, expected", KNOWN_VALUES)
def test_rabbit_known_value(n, expected):
    data = requests.get(f"{BASE_URL}/rabbit/{n}", headers=AUTH).json()
    assert data["result"] == expected


@pytest.mark.parametrize("n, expected", KNOWN_VALUES)
def test_rabbit_echoes_input(n, expected):
    data = requests.get(f"{BASE_URL}/rabbit/{n}", headers=AUTH).json()
    assert data["input"] == n


def test_rabbit_returns_200():
    r = requests.get(f"{BASE_URL}/rabbit/1", headers=AUTH)
    assert r.status_code == 200


def test_rabbit_response_has_input_and_result_keys():
    data = requests.get(f"{BASE_URL}/rabbit/5", headers=AUTH).json()
    assert "input" in data
    assert "result" in data


def test_rabbit_result_is_integer():
    data = requests.get(f"{BASE_URL}/rabbit/5", headers=AUTH).json()
    assert isinstance(data["result"], int)


def test_rabbit_zero_returns_422():
    r = requests.get(f"{BASE_URL}/rabbit/0", headers=AUTH)
    assert r.status_code == 422


def test_rabbit_negative_returns_422():
    r = requests.get(f"{BASE_URL}/rabbit/-1", headers=AUTH)
    assert r.status_code == 422


def test_rabbit_no_key_returns_401():
    r = requests.get(f"{BASE_URL}/rabbit/1")
    assert r.status_code == 401


def test_rabbit_max_valid_input_returns_200():
    r = requests.get(f"{BASE_URL}/rabbit/1473", headers=AUTH)
    assert r.status_code == 200


def test_rabbit_overflow_boundary_returns_422():
    r = requests.get(f"{BASE_URL}/rabbit/1474", headers=AUTH)
    assert r.status_code == 422


def test_rabbit_large_input_returns_422():
    r = requests.get(f"{BASE_URL}/rabbit/1212121217", headers=AUTH)
    assert r.status_code == 422


def test_rabbit_wrong_key_returns_401():
    r = requests.get(f"{BASE_URL}/rabbit/1", headers={"X-API-Key": "wrong"})
    assert r.status_code == 401


def test_rabbit_sequential_results_grow():
    results = [requests.get(f"{BASE_URL}/rabbit/{n}", headers=AUTH).json()["result"] for n in range(1, 8)]
    assert results == sorted(results)


def test_rabbit_each_result_is_sum_of_two_preceding():
    results = [requests.get(f"{BASE_URL}/rabbit/{n}", headers=AUTH).json()["result"] for n in range(1, 11)]
    for i in range(2, len(results)):
        assert results[i] == results[i - 1] + results[i - 2]
