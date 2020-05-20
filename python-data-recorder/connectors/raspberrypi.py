import os
import subprocess
from pprint import pprint
import re


def cpu_temp():
    reading = subprocess.check_output("vcgencmd measure_temp", shell=True)
    pattern = r"^temp=(\d*\.\d)'C\n$"
    return re.search(pattern, reading).group(1)
