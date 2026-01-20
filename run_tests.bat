@echo off
echo ========================================
echo Running Pink Morsel Dashboard Tests
echo ========================================

python simple_test.py

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo ✅ All tests passed!
    echo ========================================
    exit /b 0
) else (
    echo ========================================
    echo ❌ Tests failed
    echo ========================================
    exit /b 1
)