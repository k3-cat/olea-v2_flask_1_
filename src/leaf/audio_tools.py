from pydub import AudioSegment


def get_audio_info(path: str) -> dict:
    sound = AudioSegment.from_file(path, format='flac')
    metadata = {
        'frame_rate': sound.frame_rate,
        'frame_width': sound.frame_width,
        'duration': sound.duration_seconds / 1000
    }
    return metadata
