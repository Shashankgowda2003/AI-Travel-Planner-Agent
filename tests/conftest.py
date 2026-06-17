import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_env_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-mock-key")
