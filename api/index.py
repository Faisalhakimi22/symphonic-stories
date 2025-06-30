import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.main import app as application

# Vercel will look for 'app' or 'application' as the entry point
# This file exposes the Flask app instance for serverless deployment 