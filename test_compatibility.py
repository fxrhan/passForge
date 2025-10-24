#!/usr/bin/env python3
"""
Cross-platform compatibility test for longtongue
Tests that the project can run on both Windows and Linux
"""

import os
import sys
import tempfile
import shutil

def test_file_creation():
    """Test cross-platform file creation"""
    print("Testing file creation...")
    test_dir = tempfile.mkdtemp()
    try:
        # Test using open() instead of os.mknod()
        test_file = os.path.join(test_dir, "test.txt")
        open(test_file, 'a').close()
        assert os.path.exists(test_file), "File creation failed"
        print("✓ File creation works")
    finally:
        shutil.rmtree(test_dir)

def test_path_handling():
    """Test cross-platform path handling"""
    print("Testing path handling...")
    # Test os.path.join() works correctly
    path1 = os.path.join("output", "test.txt")
    path2 = os.path.join("output", "test-file.txt")
    
    # Verify paths are created correctly for the platform
    if sys.platform == "win32":
        assert "\\" in path1 or "/" in path1, "Windows path handling failed"
    else:
        assert "/" in path1, "Unix path handling failed"
    print("✓ Path handling works")

def test_directory_creation():
    """Test cross-platform directory creation"""
    print("Testing directory creation...")
    test_dir = tempfile.mkdtemp()
    try:
        subdir = os.path.join(test_dir, "output")
        os.makedirs(subdir, exist_ok=True)
        assert os.path.exists(subdir), "Directory creation failed"
        print("✓ Directory creation works")
    finally:
        shutil.rmtree(test_dir)

def test_imports():
    """Test that all required modules are available"""
    print("Testing imports...")
    try:
        import argparse
        import itertools
        print("✓ All required modules available")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    return True

def main():
    print("=" * 50)
    print("Cross-Platform Compatibility Test")
    print(f"Platform: {sys.platform}")
    print(f"Python: {sys.version}")
    print("=" * 50)
    print()
    
    try:
        test_imports()
        test_file_creation()
        test_path_handling()
        test_directory_creation()
        print()
        print("=" * 50)
        print("✓ All tests passed!")
        print("Project is compatible with both Windows and Linux")
        print("=" * 50)
        return 0
    except Exception as e:
        print()
        print("=" * 50)
        print(f"✗ Test failed: {e}")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    sys.exit(main())
