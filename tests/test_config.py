import os
import pytest


class TestConfigSettings:
    def test_config_module_exists(self):
        from config import settings
        assert settings is not None

    def test_openai_api_key_required(self):
        from config import Settings
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            Settings(openai_api_key="")

    def test_model_name_default(self):
        from config import settings
        assert settings.model_name == "gpt-4"

    def test_temperature_default(self):
        from config import settings
        assert settings.temperature == 0.2

    def test_chroma_persist_dir_default(self):
        from config import settings
        assert settings.chroma_persist_dir == "./chroma_db"

    def test_origin_city_default(self):
        from config import settings
        assert settings.origin_city == "Bangalore"

    def test_default_days(self):
        from config import settings
        assert settings.default_days == 3

    def test_default_budget(self):
        from config import settings
        assert settings.default_budget == 10000

    def test_max_days(self):
        from config import settings
        assert settings.max_days == 14

    def test_google_maps_api_key_optional(self):
        from config import Settings
        s = Settings(openai_api_key="sk-test", google_maps_api_key=None)
        assert s.google_maps_api_key is None

    def test_settings_singleton(self):
        from config import settings as s1
        from config import settings as s2
        assert s1 is s2

    def test_openweather_api_key_optional(self):
        from config import Settings
        s = Settings(openai_api_key="sk-test", openweather_api_key=None)
        assert s.openweather_api_key is None

    def test_fallback_models_list(self):
        from config import settings
        assert isinstance(settings.fallback_models, list)
        assert "gpt-4" in settings.fallback_models
