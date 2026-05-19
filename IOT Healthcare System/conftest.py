import sys
import os
from unittest.mock import MagicMock

# mock mariadb before any imports happen
sys.modules['mariadb'] = MagicMock()

# add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))