import os
import pytest


class TestToolsPackageInit:
    def test_init_py_exists(self):
        init_path = os.path.join("tools", "__init__.py")
        assert os.path.exists(init_path), f"{init_path} does not exist"

    def test_package_exports_booking_search_links(self):
        from tools import booking_search_links
        assert callable(booking_search_links)

    def test_package_exports_google_maps_search_url(self):
        from tools import google_maps_search_url
        assert callable(google_maps_search_url)

    def test_package_exports_google_maps_embed_iframe_url(self):
        from tools import google_maps_embed_iframe_url
        assert callable(google_maps_embed_iframe_url)

    def test_package_has_docstring(self):
        import tools
        assert tools.__doc__ is not None, "tools package should have a docstring"
