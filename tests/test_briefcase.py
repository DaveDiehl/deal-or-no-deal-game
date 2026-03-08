import pytest
from src.briefcase import Briefcase


def test_briefcase_creation():
    b = Briefcase(5, 10000)
    assert b.number == 5
    assert b.amount == 10000


def test_briefcase_open_returns_amount():
    b = Briefcase(3, 500)
    assert b.open() == 500


def test_briefcase_open_marks_as_opened():
    b = Briefcase(1, 1000)
    b.open()
    assert b.is_opened is True


def test_briefcase_not_opened_by_default():
    b = Briefcase(2, 200)
    assert b.is_opened is False


def test_briefcase_open_twice_raises():
    b = Briefcase(7, 750)
    b.open()
    with pytest.raises(ValueError):
        b.open()


def test_briefcase_str_closed():
    b = Briefcase(5, 10000)
    assert str(b) == "Case #5"


def test_briefcase_str_opened():
    b = Briefcase(5, 10000)
    b.open()
    assert str(b) == "Case #5 ($10,000)"


def test_briefcase_equality_by_number():
    b1 = Briefcase(4, 100)
    b2 = Briefcase(4, 999)
    assert b1 == b2


def test_briefcase_inequality():
    b1 = Briefcase(1, 100)
    b2 = Briefcase(2, 100)
    assert b1 != b2
