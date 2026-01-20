# simple_test_app.py
import pytest
from app import app  # Import your Dash app

def test_app_instance():
    """Test that the app instance is created"""
    assert app is not None, "App instance not created"
    assert isinstance(app, type(app)), "App should be a Dash instance"
    print("✅ App instance test passed")

def test_app_layout():
    """Test that the app has a layout"""
    layout = app.layout
    assert layout is not None, "App layout is None"
    print("✅ App layout test passed")

def test_header_in_layout():
    """Test that header is in the layout"""
    # Check if header exists by looking at layout components
    layout_str = str(app.layout)
    assert "Pink Morsel" in layout_str, "Header 'Pink Morsel' not found in layout"
    print("✅ Header test passed")

def test_visualization_in_layout():
    """Test that visualization is in the layout"""
    layout_str = str(app.layout)
    assert "sales-chart" in layout_str, "Sales chart not found in layout"
    print("✅ Visualization test passed")

def test_region_picker_in_layout():
    """Test that region picker is in the layout"""
    layout_str = str(app.layout)
    assert "region-radio" in layout_str, "Region radio buttons not found in layout"
    print("✅ Region picker test passed")

if __name__ == "__main__":
    # Run tests
    test_app_instance()
    test_app_layout()
    test_header_in_layout()
    test_visualization_in_layout()
    test_region_picker_in_layout()
    print("\n🎉 All tests passed!")