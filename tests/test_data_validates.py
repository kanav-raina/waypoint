"""Smoke tests: every committed JSON file under data/ validates against the Pydantic schemas.

Run from repo root:
    pytest tests/

These guard the central architectural promise of the project — "drop a JSON file in
data/ and it works." If a new student or lesson file fails validation, this catches it
before the MCP server tries to load it under Claude Desktop and silently 500s.
"""

from pathlib import Path

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
from core.schemas import IEP, Lesson

DATA_ROOT = Path(__file__).parent.parent / "data"
STUDENT_FILES = sorted((DATA_ROOT / "students").glob("*.json"))
LESSON_FILES = sorted((DATA_ROOT / "lessons").glob("*.json"))


@pytest.mark.parametrize("path", STUDENT_FILES, ids=lambda p: p.stem)
def test_student_json_validates_against_iep_schema(path: Path) -> None:
    IEP.model_validate_json(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", LESSON_FILES, ids=lambda p: p.stem)
def test_lesson_json_validates_against_lesson_schema(path: Path) -> None:
    Lesson.model_validate_json(path.read_text(encoding="utf-8"))


def test_at_least_two_students_committed() -> None:
    """The README claims 'drop a JSON file = new student.' That claim is unverified
    with only one student. Keep at least two so the multi-record path is exercised."""
    assert len(STUDENT_FILES) >= 2, (
        f"Expected ≥2 student JSONs to demonstrate filesystem scaling; found {len(STUDENT_FILES)}"
    )


def test_at_least_two_lessons_committed() -> None:
    assert len(LESSON_FILES) >= 2, (
        f"Expected ≥2 lesson JSONs to demonstrate filesystem scaling; found {len(LESSON_FILES)}"
    )
