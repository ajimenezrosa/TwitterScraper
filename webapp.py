#!/usr/local/bin/python3
import os
from sys import platform

if platform.startswith('linux'):
    os.popen("sleep 1.5;xdg-open http://127.0.0.1:8000")
elif platform == 'darwin':
    os.popen("sleep 1.5;open 'http://127.0.0.1:8000'")
elif platform == 'win32':
    os.popen("sleep 1.5 && start '' http://127.0.0.1:8000")

os.system("python3 webapp/manage.py runserver")
