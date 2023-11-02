import pytest
from Backend.src import scheduler
from Backend.src.model.section import Section
from Backend.src.model.course import Course
from Backend.src.model.date import Date
from Backend.src.model.day_of_week import DayOfWeek

def test_is_section_schedulable():
    '''
    Tests that isSectionShedulable can handle overlaping classes and schedulable classes
    '''
    section1 = Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", [])
    section2 = Section("CODE2000", "B", "22222", "Bob", [Date(DayOfWeek.TUESDAY, "09:05", "10:35"), Date(DayOfWeek.THURSDAY, "09:05", "10:35") ], "", [])
    section3 = Section("CODE3000", "C", "33333", "Charlie", [Date(DayOfWeek.FRIDAY, "09:05", "10:35")], "", [])
    schedule = [
        Section("CODE4000", "D", "44444", "Dom", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", []),
        Section("CODE5000", "E", "55555", "Eric", [Date(DayOfWeek.MONDAY, "11:05", "12:35"), Date(DayOfWeek.THURSDAY,"10:05", "11:35") ], "", [])
    ]
    assert scheduler.is_section_schedulable(section1, schedule) == False
    assert scheduler.is_section_schedulable(section2, schedule) == False
    assert scheduler.is_section_schedulable(section3, schedule) == True


def test_can_take_together():
    '''
    Testing if a lecture and lab section are compatible to take together
    '''
    LECTURE_SECTION_ID = "A"
    LAB_SECTION_ID = "L01"
    lecture_section = Section("CODE1234", LECTURE_SECTION_ID, "54321", "Jill", [], "", [LAB_SECTION_ID])
    lab_section = Section("CODE1234", LAB_SECTION_ID, "54321", "Jill", [], "", ["Z", "Q", LECTURE_SECTION_ID])
    assert scheduler.can_take_together(lecture_section, lab_section) == True
    lecture_section.related_section_ids.pop()
    assert scheduler.can_take_together(lecture_section, lab_section) == False
    assert scheduler.can_take_together(lab_section, lecture_section) == True


def test_generate_schedules_with_no_courses():
    '''
    Tests that generateSchedules function can handle empty courses list
    '''
    schedule = [
        Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", [])
    ]
    assert scheduler.generate_schedules([], schedule) == [schedule]


def test_generate_schedules_with_lab_sections():
    '''
    Tests that the generateSchedules function can schedule courses with lab sections
    '''
    section1 = Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", ["L1"])
    section2 = Section("CODE1000", "L1", "12345", "Alice", [Date(DayOfWeek.TUESDAY, "09:05", "10:35")], "", ["A"])
    section3 = Section("CODE4000", "D", "44444", "Dom", [Date(DayOfWeek.THURSDAY, "09:05", "10:35"), Date(DayOfWeek.FRIDAY, "09:05", "10:35") ], "", [])
    section4 = Section("CODE5000", "E", "55555", "Eric", [Date(DayOfWeek.MONDAY, "11:05", "12:35"), Date(DayOfWeek.THURSDAY,"12:05", "13:35") ], "", [])
    course1 = Course("CODE1000", "TESTCLASS", "Fall 2023", "NONE", [section1], [section2], None)
    schedule1 = [
        section3, section4
    ]
    expected_schedule = [
       section3, section4, section1, section2
    ]
    assert scheduler.generate_schedules([course1], schedule1) == [expected_schedule]


def test_generate_schedules_without_lab_sections():
    '''
    Test that the generateSchedules function can schedule courses without lab section
    '''
    section1 = Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", [])
    section2 = Section("CODE4000", "D", "44444", "Dom", [Date(DayOfWeek.THURSDAY, "09:05", "10:35"), Date(DayOfWeek.FRIDAY, "09:05", "10:35") ], "", [])
    section3 = Section("CODE5000", "E", "55555", "Eric", [Date(DayOfWeek.MONDAY, "11:05", "12:35"), Date(DayOfWeek.THURSDAY,"12:05", "13:35") ], "", [])
    course1 = Course("CODE1000", "TESTCLASS", "Fall 2023", "NONE", [section1], [], None)
    schedule1 = [
        section2, section3
    ]
    expected_schedule = [
        section2,
        section3,
        section1
    ]
    assert scheduler.generate_schedules([course1], schedule1) == [expected_schedule]

def test_generate_schedules_with_incompatible_lab():
    '''
    Tests the generateSchedules function withincomptible lecture/lab sections
    '''
    section1 = Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", ["A1"])
    section2 = Section("CODE1000", "A1", "12345", "Alice", [Date(DayOfWeek.FRIDAY, "09:05", "10:35")], "", ["A"])
    section3 = Section("CODE1000", "B1", "44444", "Dom", [Date(DayOfWeek.THURSDAY, "09:05", "10:35")], "", ["B"])
    course1 = Course("CODE1000", "TESTCLASS", "Fall 2023", "NONE", [section1], [section2, section3], None)
    expected_schedule = [
       section1, section2
    ]
    assert scheduler.generate_schedules([course1]) == [expected_schedule]


def test_generate_schedules_with_unschedulable_section():
    '''
    Tests  the generateSchedules function unschedulable lecture AND lab section
    '''
    section1 = Section("CODE1000", "A", "11111", "Alice", [Date(DayOfWeek.MONDAY, "09:05", "10:35"), Date(DayOfWeek.WEDNESDAY, "09:05", "10:35") ], "", ["L1"])
    section2 = Section("CODE1000", "L1", "12345", "Alice", [Date(DayOfWeek.MONDAY, "11:05", "13:55")], "", ["A"])
    section3 = Section("CODE4000", "D", "44444", "Dom", [Date(DayOfWeek.THURSDAY, "12:05", "13:35"), Date(DayOfWeek.FRIDAY, "09:05", "10:35") ], "", [])
    section4 = Section("CODE5000", "E", "55555", "Eric", [Date(DayOfWeek.MONDAY, "11:05", "12:35"), Date(DayOfWeek.THURSDAY,"12:05", "13:35") ], "", [])
    course1 = Course("CODE1000", "TESTCLASS", "Fall 2023", "NONE", [section1], [section2], None)
    course2 = Course("CODE4000", "TESTCLASS2", "Fall 2023", "NONE", [section3], [], None)
    schedule1 = [
        section4
    ]
    assert scheduler.generate_schedules([course1], schedule1) == []
    assert scheduler.generate_schedules([course2], schedule1) == []


