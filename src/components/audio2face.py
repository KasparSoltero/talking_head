from io import BytesIO
import time
from typing import Generator
import grpc
import py_audio2face as pya2f
import numpy as np

from src.components import audio2face_pb2, audio2face_pb2_grpc
from src.components.text_to_speech import SAMPLERATE


# PORT = 12031
PORT = 50051


class Audio2FaceController:
    a2f: pya2f.Audio2Face

    def __init__(self):
        pass
        self.a2f = pya2f.Audio2Face(f"localhost:{PORT}")
        # self.a2f.init_a2f()

    def play_animation_from_audio(self, audio_data: BytesIO):
        # self.play_animation_from_audio_stream([audio_data])
        bytes = audio_data.getvalue()
        push_audio_track(
            "localhost:50051",
            bytes,
            44100,
            # "/World/audio2face/receive_audio_stream",
            "/World/audio2face/PlayerStreaming",
        )

    def play_animation_from_audio_stream(
        self, audio_stream: Generator[np.ndarray | bytes, None, None]
    ):
        # self.a2f.init_a2f()
        push_audio_track_stream(
            "localhost:50051",
            audio_stream,
            SAMPLERATE,
            # "/World/audio2face/receive_audio_stream",
            "/World/audio2face/PlayerStreaming",
        )
        # self.a2f.stream_audio(audio_data, 44100)
        # # push_audio_track(
        # #     "localhost:50051",
        # #     audio_data,
        # #     44100,
        # #     "/World/audio2face/receive_audio_stream",
        # # )


def push_audio_track(url, audio_data: bytes, samplerate, instance_name):
    """
    This function pushes the whole audio track at once via PushAudioRequest()
    PushAudioRequest parameters:
     * audio_data: bytes, containing audio data for the whole track, where each sample is encoded as 4 bytes (float32)
     * samplerate: sampling rate for the audio data
     * instance_name: prim path of the Audio2Face Streaming Audio Player on the stage, were to push the audio data
     * block_until_playback_is_finished: if True, the gRPC request will be blocked until the playback of the pushed track is finished
    The request is passed to PushAudio()
    """

    block_until_playback_is_finished = False  # ADJUST
    with grpc.insecure_channel(url) as channel:
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
        request = audio2face_pb2.PushAudioRequest()
        request.audio_data = audio_data
        request.samplerate = samplerate
        request.instance_name = instance_name
        request.block_until_playback_is_finished = block_until_playback_is_finished
        print("Sending audio data...")
        response = stub.PushAudio(request)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")
    print("Closed channel")


def push_audio_track_stream(url, audio_data, samplerate, instance_name):
    """
    This function pushes audio chunks sequentially via PushAudioStreamRequest()
    The function emulates the stream of chunks, generated by splitting input audio track.
    But in a real application such stream of chunks may be aquired from some other streaming source.
    The first message must contain start_marker field, containing only meta information (without audio data):
     * samplerate: sampling rate for the audio data
     * instance_name: prim path of the Audio2Face Streaming Audio Player on the stage, were to push the audio data
     * block_until_playback_is_finished: if True, the gRPC request will be blocked until the playback of the pushed track is finished (after the last message)
    Second and other messages must contain audio_data field:
     * audio_data: bytes, containing audio data for an audio chunk, where each sample is encoded as 4 bytes (float32)
    All messages are packed into a Python generator and passed to PushAudioStream()
    """

    chunk_size = samplerate // 10  # ADJUST
    sleep_between_chunks = 0.04  # ADJUST
    block_until_playback_is_finished = True  # ADJUST

    with grpc.insecure_channel(url) as channel:
        print("Channel creadted")
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=samplerate,
                instance_name=instance_name,
                block_until_playback_is_finished=block_until_playback_is_finished,
            )
            # At first, we send a message with start_marker
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
            # Then we send messages with audio_data
            for i in range(len(audio_data) // chunk_size + 1):
                time.sleep(sleep_between_chunks)
                chunk = audio_data[i * chunk_size : i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(
                    audio_data=chunk.astype(np.float32).tobytes()
                )

        request_generator = make_generator()
        print("Sending audio data...")
        response = stub.PushAudioStream(request_generator)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")
    print("Channel closed")
