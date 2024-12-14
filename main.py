import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
libs_path = os.path.join(current_dir, 'libs')
sys.path.insert(0, libs_path)

from video_server import app


