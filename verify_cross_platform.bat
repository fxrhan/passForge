@echo off
REM Cross-platform verification script for Windows
REM Run this on Windows to verify compatibility

echo ==================================
echo Cross-Platform Verification Script
echo Platform: Windows
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Run compatibility tests
echo Running compatibility tests...
python test_compatibility.py
echo.

REM Test basic commands
echo Testing basic commands...
echo 1. Version check:
python longtongue.py -v
echo.

echo 2. Help display:
python longtongue.py -h
echo.

echo ==================================
echo Verification complete!
echo ==================================
pause
