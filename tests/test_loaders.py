"""Tests for the data loader: discovery, section access, error handling."""

import pytest

from core.data_loader import (
    IEP_SECTIONS,
    get_iep_section,
    get_lesson_part,
    list_lessons,
    list_students,
    load_iep,
    load_lesson,
)


def test_list_students_returns_all_committed_students() -> None:
    students = list_students()
    ids = {s["student_id"] for s in students}
    assert "jasmine_bailey" in ids
    assert "marcus_chen" in ids
    for s in students:
        assert {"student_id", "name", "grade", "disability"} <= set(s.keys())


def test_list_lessons_returns_all_committed_lessons() -> None:
    lessons = list_lessons()
    ids = {l["lesson_id"] for l in lessons}
    assert "unit1_lesson1" in ids
    assert "unit1_lesson2" in ids
    for l in lessons:
        assert {"lesson_id", "title", "subject", "grade", "duration_minutes"} <= set(l.keys())


def test_load_iep_unknown_student_raises_with_helpful_message() -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        load_iep("nonexistent_student")
    # The message should list available IDs so Claude (or a developer) can recover.
    assert "Available" in str(excinfo.value)


def test_load_lesson_unknown_lesson_raises_with_helpful_message() -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        load_lesson("nonexistent_lesson")
    assert "Available" in str(excinfo.value)


@pytest.mark.parametrize("section", list(IEP_SECTIONS.keys()))
def test_get_iep_section_returns_data_for_every_known_section(section: str) -> None:
    """Every section name advertised in the tool docstring must actually resolve."""
    result = get_iep_section("jasmine_bailey", section)
    assert result is not None
    # Sections return either a dict (single record) or a list (collection).
    assert isinstance(result, (dict, list))


def test_get_iep_section_rejects_unknown_section() -> None:
    with pytest.raises(ValueError) as excinfo:
        get_iep_section("jasmine_bailey", "not_a_real_section")
    assert "Available" in str(excinfo.value)


def test_get_lesson_part_returns_each_advertised_part_name() -> None:
    """The server.py docstring advertises four parts; this guards that they all exist."""
    advertised = ["intro", "during_reading", "independent_practice", "discussion"]
    for part in advertised:
        result = get_lesson_part("unit1_lesson1", part)
        assert result["name"] == part


def test_get_lesson_part_rejects_unknown_part() -> None:
    with pytest.raises(ValueError) as excinfo:
        get_lesson_part("unit1_lesson1", "not_a_real_part")
    assert "Available" in str(excinfo.value)
