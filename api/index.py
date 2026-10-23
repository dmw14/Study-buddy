import os
import sys

# Add repository root to Python path so main and its modules are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
