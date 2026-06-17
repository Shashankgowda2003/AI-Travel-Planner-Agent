import ast
import pytest
from pathlib import Path


AGENT_PATH = Path(__file__).resolve().parent.parent / "agent.py"

DEAD_IMPORTS = [
    "initialize_agent",
    "AgentType",
]

DEAD_TOOLS = [
    "booking_tool",
    "maps_tool",
]

USEFUL_IMPORTS = [
    "ChatOpenAI",
    "OpenAIEmbeddings",
    "Chroma",
    "Document",
    "PromptTemplate",
    "LLMChain",
    "ConversationBufferMemory",
]


def _parse_agent_source():
    source = AGENT_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_names = set()
    assigned_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name
                imported_names.add(name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                imported_names.add(name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_names.add(target.id)

    return imported_names, assigned_names


class TestAgentNoDeadCode:
    """Verify agent.py has no dead imports or dead Tool objects."""

    @staticmethod
    def _parsed():
        return _parse_agent_source()

    @pytest.mark.parametrize("name", DEAD_IMPORTS)
    def test_dead_import_removed(self, name):
        imported_names, _ = self._parsed()
        assert name not in imported_names, (
            f"Dead import '{name}' still present in agent.py — remove it"
        )

    @pytest.mark.parametrize("name", DEAD_TOOLS)
    def test_dead_tool_removed(self, name):
        _, assigned_names = self._parsed()
        assert name not in assigned_names, (
            f"Dead Tool '{name}' still present in agent.py — remove it"
        )

    @pytest.mark.parametrize("name", USEFUL_IMPORTS)
    def test_useful_imports_preserved(self, name):
        imported_names, _ = self._parsed()
        assert name in imported_names, (
            f"Useful import '{name}' is missing from agent.py"
        )

    def test_optional_str_imported(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert "from typing import" in source
        assert "Optional" in source

    def test_no_persist_call(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert ".persist()" not in source

    def test_api_key_validation_present(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert "if not OPENAI_API_KEY:" in source

    def test_response_format_json_object(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert '"response_format"' in source
        assert '"json_object"' in source

    def test_structured_logging_imported(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert "import logging" in source

    def test_india_destinations_referenced(self):
        source = AGENT_PATH.read_text(encoding="utf-8")
        assert "india_destinations.json" in source
