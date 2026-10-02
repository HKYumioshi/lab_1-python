import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError

#позитивные тесты

def test_convert_length_cm_to_m():
    assert convert(250, "cm", "m") == 2.5


def test_convert_weight_g_to_kg():
    assert convert(1500, "g", "kg") == 1.5


def test_convert_celsius_to_fahrenheit():
    assert convert(0, "c", "f") == 32.0


def test_convert_kelvin_to_celsius():
    assert convert(273.15, "k", "c") == pytest.approx(0.0)


def test_convert_result_is_float():
    assert isinstance(convert(10, "mm", "cm"), float)


#негативные тесты

def test_convert_unknown_unit_raises():
    with pytest.raises(ConverterError):
        convert(10, "mm", "banana")


def test_convert_incompatible_groups_raises():
    with pytest.raises(ConverterError):
        convert(10, "cm", "kg")


def test_convert_below_absolute_zero_celsius_raises():
    with pytest.raises(ConverterError):
        convert(-300, "c", "f")


def test_convert_below_absolute_zero_fahrenheit_raises():
    with pytest.raises(ConverterError):
        convert(-1000, "f", "c")
