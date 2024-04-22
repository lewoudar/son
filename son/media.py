import re
import subprocess
from datetime import datetime, timedelta


def get_seconds_from_str_time(str_time: str) -> float:
    """Converts a string time in format hh:mm:ss.ss into seconds"""
    time_format = datetime.strptime(str_time, '%H:%M:%S.%f')
    delta = timedelta(
        hours=time_format.hour,
        minutes=time_format.minute,
        seconds=time_format.second,
        microseconds=time_format.microsecond,
    )
    return delta.total_seconds()


def get_media_duration(filename: str) -> float:
    result = subprocess.run(['ffmpeg', '-i', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode()
    matches = re.search(r'Duration: (\d{2}:\d{2}:\d{2}.\d{2})', output)
    if matches:
        return get_seconds_from_str_time(matches.group(1))
