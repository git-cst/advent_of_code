from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution