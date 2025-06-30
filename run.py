#!/usr/bin/env python3
"""
Symphonic Stories - Startup Script
Run this script to start the application
"""

import os
import sys
from src.main import main

if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the main function
    main() 