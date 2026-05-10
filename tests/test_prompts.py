"""Tests for prompt construction.

The system prompt is the highest-leverage piece of the project. These tests guard the
specific behavior-shaping rules from being silently weakened in a refactor.
"""

import json

from core.prompts import (
    DIFFERENTIATION_SYSTEM_PROMPT,
    build_differentiation_prompt,
    build_quick_summary_prompt,
)


def test_system_prompt_enforces_grounding_rule() -> None:
    """Rule 1: every modification must cite an accommodation, modification, goal,
    or present-level finding. Without this the output regresses to UDL platitudes."""
    p = DIFFERENTIATION_SYSTEM_PROMPT.lower()
    assert "accommodation" in p
    assert "modification" in p, "Rule 1 must mention modifications (legally distinct from accommodations)"
    assert "goal" in p
    assert "present" in p


def test_system_prompt_enforces_specific_lesson_references() -> None:
    """Rule 2: must reference specific paragraphs/questions, not 'scaffold the reading.'"""
    p = DIFFERENTIATION_SYSTEM_PROMPT.lower()
    assert "paragraph" in p or "question" in p


def test_system_prompt_locks_output_structure() -> None:
    """Rule 6: output structure must be enumerated explicitly, not just implied,
    so output is consistent across runs and across students."""
    p = DIFFERENTIATION_SYSTEM_PROMPT.lower()
    assert "materials" in p, "Materials checklist must be required"
    assert "pacing" in p or "phase" in p or "part" in p


def test_build_differentiation_prompt_embeds_both_documents() -> None:
    prompt = build_differentiation_prompt("jasmine_bailey", "unit1_lesson1")
    assert "STUDENT IEP" in prompt
    assert "LESSON" in prompt
    # IEP-specific content
    assert "Jasmine" in prompt
    # Lesson-specific content
    assert "community" in prompt.lower()


def test_build_differentiation_prompt_works_for_second_student_lesson_pair() -> None:
    """Multi-record sanity check: the prompt builder must work for any (student, lesson)
    combination, not just the original Jasmine + unit1_lesson1 pair."""
    prompt = build_differentiation_prompt("marcus_chen", "unit1_lesson2")
    assert "Marcus" in prompt
    assert "RL.7.2" in prompt or "Welcome Table" in prompt


def test_quick_summary_prompt_constrains_length() -> None:
    """Substitute-teacher use case: the response must fit on a phone screen."""
    prompt = build_quick_summary_prompt("jasmine_bailey")
    assert "200 words" in prompt or "under 200" in prompt
