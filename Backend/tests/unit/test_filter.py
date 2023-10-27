import pytest
from Backend.src.model.filter import Filter
from Backend.src.model.day_of_week import DayOfWeek

def test_create_empty_filter():
    filter = Filter()
    assert filter.before_time == None
    assert filter.after_time == None
    assert filter.day_of_week == None

def test_create_filter():
    filter = Filter(before_time = "09:00", after_time = "14:00", day_of_week = DayOfWeek.MONDAY)
    assert filter.before_time == "09:00"
    assert filter.after_time == "14:00"
    assert filter.day_of_week == DayOfWeek.MONDAY

def test_invalid_before_time():
    with pytest.raises(TypeError):
        Filter(before_time = 4)

def test_invalid_after_time():
    with pytest.raises(TypeError):
        Filter(after_time = ["12:00"])

def test_invalid_day_of_week():
    with pytest.raises(TypeError):
        Filter(day_of_week = "MONDAY")