from typing import List
from pydub import AudioSegment

def merge_audio_files(audio_files: List[str]) -> str:
    """
    Merge multiple audio files into a single podcast episode.

    Args:
        audio_files (List[str]): A list of file paths to the audio files to merge.

    Returns:
        str: The file path of the merged podcast episode.
    """
    combined: AudioSegment = AudioSegment.empty()
    for file in audio_files:
        audio: AudioSegment = AudioSegment.from_mp3(file)
        combined += audio
        combined += AudioSegment.silent(duration=1000)  # 1 second silence between summaries

    output_path: str = "final_podcast.mp3"
    combined.export(output_path, format="mp3")
    return output_path
