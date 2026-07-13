import pytest
import os
from unittest.mock import MagicMock, patch
from app import get_system_instruction, get_secure_gemini_client, sanitize_user_input

def test_fan_system_instruction_generation():
    """Ensures the Spectator agent logic loads language constraints and target pillars."""
    instruction = get_system_instruction("Spectator / Fan", "Português")
    assert "StadiumPulse Fan Assist" in instruction
    assert "Português" in instruction
    assert "Gate C" in instruction

def test_staff_system_instruction_generation():
    """Ensures the Staff operational layout loads structural triage headers."""
    instruction = get_system_instruction("Stadium Staff / Volunteer", "English")
    assert "StadiumPulse Ops Commander" in instruction
    assert "Severity Level" in instruction
    assert "Immediate Mitigation Action" in instruction
    assert "Resource Allocation Suggestion" in instruction

@pytest.mark.parametrize("input_string, expected_output", [
    ("<script>test</script>", "scripttestscript"),
    ("Help me with [Gate A] layout", "Help me with Gate A layout"),
    ("Valid raw question string without syntax anomalies.", "Valid raw question string without syntax anomalies."),
    ("", "")
])
def test_input_sanitization_engine(input_string, expected_output):
    """Validates that potential injection signatures are filtered correctly."""
    assert sanitize_user_input(input_string) == expected_output

def test_input_truncation_security_limit():
    """Confirms that input parameters exceeding length limits are truncated."""
    excessive_input = "A" * 600
    sanitized_output = sanitize_user_input(excessive_input)
    assert len(sanitized_output) == 500

def test_client_fallback_with_missing_keys():
    """Verifies environment parameter fallback logic when credentials are absent."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        client_instance = get_secure_gemini_client()
        assert client_instance is None
