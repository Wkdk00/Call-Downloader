from mutagen.mp3 import MP3
from io import BytesIO

def duration(b_file: bytes) -> str:
    file = BytesIO(b_file)
    audio = MP3(file)
    dur = audio.info.length
    if dur < 3*60: value = "short"
    elif dur < 6*60: value = "middle"
    else: value = "long"
    file.seek(0)
    return value