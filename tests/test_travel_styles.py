import pytest


class TestTravelStyles:
    def test_travel_styles_in_config(self):
        from config import TRAVEL_STYLES, STYLE_PROMPTS
        assert isinstance(TRAVEL_STYLES, list)
        assert len(TRAVEL_STYLES) >= 6
        assert "luxury" in TRAVEL_STYLES
        assert "budget" in TRAVEL_STYLES
        assert "adventure" in TRAVEL_STYLES
        assert isinstance(STYLE_PROMPTS, dict)

    def test_style_prompts_have_all_styles(self):
        from config import TRAVEL_STYLES, STYLE_PROMPTS
        for style in TRAVEL_STYLES:
            assert style in STYLE_PROMPTS, f"{style} missing from STYLE_PROMPTS"

    def test_style_prompts_are_different(self):
        from config import STYLE_PROMPTS
        values = list(STYLE_PROMPTS.values())
        assert len(set(values)) == len(values), "Style prompts should be unique"

    def test_style_budget_weights(self):
        from config import STYLE_BUDGET_WEIGHTS
        assert isinstance(STYLE_BUDGET_WEIGHTS, dict)
        for style, weights in STYLE_BUDGET_WEIGHTS.items():
            assert "stay" in weights
            assert "food" in weights
            assert "activities" in weights
            assert "travel" in weights
            total = sum(weights.values())
            assert 0.95 <= total <= 1.05, f"{style} weights should sum to ~1.0"


class TestDietaryFilters:
    def test_dietary_options_defined(self):
        from config import DIETARY_OPTIONS, ACCESSIBILITY_OPTIONS
        assert isinstance(DIETARY_OPTIONS, list)
        assert isinstance(ACCESSIBILITY_OPTIONS, list)
        assert len(DIETARY_OPTIONS) >= 4
        assert len(ACCESSIBILITY_OPTIONS) >= 3

    def test_dietary_filter_inclusion(self):
        filters = ["Vegetarian", "Wheelchair accessible"]
        prompt_adj = _build_filter_text(filters)
        assert "Vegetarian" in prompt_adj
        assert "Wheelchair" in prompt_adj


def _build_filter_text(filters: list[str]) -> str:
    dietary = [f for f in filters if f in ["Vegetarian", "Vegan", "Halal", "Gluten-free", "Jain"]]
    accessibility = [f for f in filters if f in ["Wheelchair accessible", "Child-friendly", "Senior-friendly", "Low physical activity"]]
    parts = []
    if dietary:
        parts.append(f"Dietary: {', '.join(dietary)}.")
    if accessibility:
        parts.append(f"Accessibility: {', '.join(accessibility)}.")
    return " ".join(parts)
