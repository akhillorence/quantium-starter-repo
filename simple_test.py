#!/usr/bin/env python3
"""
Simple test runner for Pink Morsel Dashboard
This bypasses pytest-dash issues and runs basic validation tests
"""

import sys
import os

def test_app_exists():
    """Test that app.py exists and can be imported"""
    try:
        import app
        print("✅ Test 1: App imports successfully")
        return app
    except ImportError as e:
        print(f"❌ Test 1: Failed to import app - {e}")
        return None

def test_app_has_layout(app_instance):
    """Test that the app has a layout"""
    if hasattr(app_instance, 'app'):
        app_obj = app_instance.app
    else:
        app_obj = app_instance
    
    if hasattr(app_obj, 'layout'):
        print("✅ Test 2: App has layout")
        return str(app_obj.layout)
    else:
        print("❌ Test 2: App has no layout")
        return None

def test_header_present(layout_str):
    """Test that header is in the layout"""
    if layout_str and 'Pink Morsel' in layout_str:
        print("✅ Test 3: Header is present")
        return True
    else:
        print("❌ Test 3: Header not found")
        return False

def test_visualization_present(layout_str):
    """Test that visualization is in the layout"""
    if layout_str and 'sales-chart' in layout_str:
        print("✅ Test 4: Visualization is present")
        return True
    else:
        print("❌ Test 4: Visualization not found")
        return False

def test_region_picker_present(layout_str):
    """Test that region picker is in the layout"""
    if layout_str and 'region-radio' in layout_str:
        print("✅ Test 5: Region picker is present")
        return True
    else:
        print("❌ Test 5: Region picker not found")
        return False

def run_all_tests():
    """Run all tests and return success/failure"""
    print("=" * 50)
    print("Running Pink Morsel Dashboard Tests")
    print("=" * 50)
    
    # Test 1: App exists
    app_instance = test_app_exists()
    if not app_instance:
        return False
    
    # Test 2: App has layout
    layout_str = test_app_has_layout(app_instance)
    if not layout_str:
        return False
    
    # Test 3-5: Check components
    tests_passed = 0
    tests_passed += 1 if test_header_present(layout_str) else 0
    tests_passed += 1 if test_visualization_present(layout_str) else 0
    tests_passed += 1 if test_region_picker_present(layout_str) else 0
    
    print("=" * 50)
    if tests_passed == 3:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {3 - tests_passed} test(s) failed")
        return False

if __name__ == "__main__":
    if run_all_tests():
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure