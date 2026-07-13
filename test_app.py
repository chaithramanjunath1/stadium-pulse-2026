import pytest
from app import get_system_instruction

def test_fan_system_instruction_incorporation():
    """Validates that the fan persona correctly configures the requested language."""
    instruction = get_system_instruction("Spectator / Fan", "Español")
    assert "StadiumPulse Fan Assist" in instruction
    assert "Español" in instruction

def test_staff_system_instruction_incorporation():
    """Validates that the staff persona includes deterministic operational headers."""
    instruction = get_system_instruction("Stadium Staff / Volunteer", "English")
    assert "StadiumPulse Ops Commander" in instruction
    assert "Severity Level" in instruction
    assert "Immediate Mitigation Action" in instruction
