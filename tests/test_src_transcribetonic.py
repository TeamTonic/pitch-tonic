# tests/test_transcribetonic.py

import pytest
import torch
from transcribetonic import TranscribeTonic

@pytest.fixture(scope='module')
def transcriber():
    return TranscribeTonic()

@pytest.mark.parametrize("audio_file, expected_text", [
    ("sample1.wav", "Hello, how are you?"),
    ("sample2.wav", "Testing the transcription."),
])
def test_transcribe(transcriber, audio_file, expected_text):
    result = transcriber.transcribe(audio_file)
    assert result == expected_text

def test_transcribe_with_invalid_audio_file(transcriber):
    with pytest.raises(Exception):
        transcriber.transcribe("invalid.wav")

def test_device_check():
    transcriber = TranscribeTonic()
    assert transcriber.model.device.type in ['cpu', 'cuda']

def test_torch_dtype():
    transcriber = TranscribeTonic()
    assert transcriber.model.dtype in [torch.float16, torch.float32]