#!/usr/bin/env python3
"""
Simple test to verify the environment is working
"""

import sys
import subprocess

def test_imports():
    """Test key imports"""
    try:
        import pandas as pd
        import numpy as np
        import requests
        import sqlite3
        print("✅ Core imports successful")
        
        import streamlit as st
        import plotly.express as px
        print("✅ Dashboard imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (id INTEGER, name TEXT)')
        cursor.execute('INSERT INTO test VALUES (1, "Test")')
        result = cursor.fetchall()
        conn.close()
        print("✅ Database functionality working")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("🚀 Testing Startup Revenue Insights Tracker Environment")
    print("=" * 60)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    success = True
    success &= test_imports()
    success &= test_database()
    
    if success:
        print("\n✅ Environment test completed successfully!")
        print("You can now run:")
        print("  python startup_tracker.py  # For data collection")
        print("  streamlit run dashboard.py  # For the dashboard")
    else:
        print("\n❌ Environment test failed. Please check dependencies.")
    
    return success

if __name__ == "__main__":
    main()