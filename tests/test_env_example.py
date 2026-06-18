import os
import pytest


REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "GOOGLE_MAPS_API_KEY",
    "CHROMA_PERSIST_DIR",
    "ORIGIN_CITY",
    "MODEL_NAME",
]


class TestEnvExample:
    def test_env_example_exists(self):
        path = os.path.join(os.path.dirname(__file__), "..", ".env.example")
        assert os.path.exists(path), ".env.example does not exist"

    def test_env_example_has_all_keys(self):
        path = os.path.join(os.path.dirname(__file__), "..", ".env.example")
        content = open(path, encoding="utf-8").read()
        for key in REQUIRED_KEYS:
            assert key in content, f"{key} missing from .env.example"

    def test_env_example_has_no_real_values(self):
        path = os.path.join(os.path.dirname(__file__), "..", ".env.example")
        content = open(path, encoding="utf-8").read()
        assert "sk-REAL" not in content, ".env.example should not contain real API keys"
        assert "your_" in content.lower() or "placeholder" in content.lower() or "replace" in content.lower(), (
            ".env.example should use placeholder values"
        )

    def test_env_example_has_comments(self):
        path = os.path.join(os.path.dirname(__file__), "..", ".env.example")
        content = open(path, encoding="utf-8").read()
        assert "#" in content, ".env.example should include explanatory comments"
