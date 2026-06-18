import pytest
from unittest.mock import patch, MagicMock


class TestBudgetOptimization:
    def test_optimize_function_exists(self):
        from agent import plan_trip_optimized
        assert callable(plan_trip_optimized)

    def test_optimize_accepts_params(self):
        from agent import plan_trip_optimized
        import inspect
        sig = inspect.signature(plan_trip_optimized)
        params = list(sig.parameters.keys())
        assert "destination" in params
        assert "days" in params
        assert "budget" in params

    @patch("agent.plan_trip_with_agent")
    def test_optimize_calls_plan_trip_twice(self, mock_plan):
        mock_plan.return_value = {
            "itinerary": ["Day 1: Beach", "Day 2: Fort"],
            "budget": {"travel": 2000, "stay": 3000, "food": 2000, "activities": 2000, "buffer": 1000},
            "links": {"booking": {}, "maps_search": ""},
            "packing_list": ["Clothing: Light clothes"],
        }
        from agent import plan_trip_optimized
        result = plan_trip_optimized("Goa", 3, 10000)
        assert mock_plan.call_count >= 2
        assert isinstance(result, dict)
        assert "itinerary" in result

    @patch("agent.plan_trip_with_agent")
    def test_optimize_returns_budget(self, mock_plan):
        mock_plan.return_value = {
            "itinerary": ["Day 1: Tour"],
            "budget": {"travel": 2000, "stay": 3000, "food": 2000, "activities": 2000, "buffer": 1000},
            "links": {"booking": {}, "maps_search": ""},
        }
        from agent import plan_trip_optimized
        result = plan_trip_optimized("Jaipur", 2, 8000)
        assert "budget" in result
        assert isinstance(result["budget"], dict)
