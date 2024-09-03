import os

ffmpeg_path = (
    r"C:\Users\edeet\Downloads\ffmpeg-7.0.2-full_build\ffmpeg-7.0.2-full_build\bin"
)
os.environ["PATH"] += os.pathsep + ffmpeg_path


from pydub import AudioSegment

AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")

audio = AudioSegment.from_file(
    r"C:\Users\edeet\Documents\talking_head\src\data\example_sentences\output_0.mp3"
)
print(f"success")
