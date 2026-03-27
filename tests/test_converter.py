import pytest
from src.converter import celsius_to_fahrenheit, celsius_to_kelvin, convert

# ── Basic tests using fixtures ──────────────────────────────────


def test_freezing_c_to_f(freezing_point):
    # freezing_point is injected from conftest.py
    assert celsius_to_fahrenheit(freezing_point["C"]) == freezing_point["F"]


def test_boiling_c_to_f(boiling_point):
    assert celsius_to_fahrenheit(boiling_point["C"]) == boiling_point["F"]


# ── Parametrize for multiple conversion cases ───────────────────

@pytest.mark.parametrize("c, expected_f", [
    (0,    32.0),   # freezing
    (100,  212.0),  # boiling
    (-40,  -40.0),  # where C and F are equal
    (37,   98.6),   # body temperature
])
def test_c_to_f_cases(c, expected_f):
    assert celsius_to_fahrenheit(c) == pytest.approx(expected_f, rel=1e-3)


# ── Edge cases ──────────────────────────────────────────────────

@pytest.mark.edge
def test_absolute_zero_kelvin():
    assert celsius_to_kelvin(-273.15) == pytest.approx(0.0)


@pytest.mark.edge
def test_below_absolute_zero_raises():
    with pytest.raises(ValueError):
        celsius_to_kelvin(-300)


# TODO: add more tests to reach ≥ 80% coverage!
# Suggestions:
#   - test fahrenheit_to_celsius
#   - test kelvin_to_celsius
#   - test convert() for all 6 unit-pair combinations
#   - test convert() with same-unit (e.g. 'C' → 'C')
#   - test convert() raises ValueError for unknown unit 'X'
#   - test negative Kelvin raises ValueError

@pytest.fixture
def freezing_point():
    return {"C": 0.0, "F": 32.0, "K": 273.15}


def test_freezing_c_to_k(freezing_point):  # ← name matches fixture
    assert (
        celsius_to_kelvin(freezing_point["C"])
        == pytest.approx(freezing_point["K"])
    )


@pytest.mark.parametrize("value, from_u, to_u, expected", [
    (0,      "C", "F", 32.0),      # C → F
    (32,     "F", "C", 0.0),       # F → C
    (0,      "C", "K", 273.15),   # C → K
    (273.15, "K", "C", 0.0),       # K → C
    (32,     "F", "K", 273.15),   # F → K
    (273.15, "K", "F", 32.0),      # K → F
])
def test_convert_all_pairs(value, from_u, to_u, expected):
    assert convert(value, from_u, to_u) == pytest.approx(expected, rel=1e-3)


# def test_negative_kelvin_raises():
#     with pytest.raises(ValueError):
#         kelvin_to_celsius(-1)   # this should raise ValueError


def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert(100, "C", "X")   # 'X' is not a valid unit
