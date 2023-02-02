import replicate
import os
import io
import json


def speach_to_text(audio):

    model = replicate.models.get("openai/whisper")
    version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
    inputs = {
        # Audio file
        'audio': open(audio, "rb"),

        # Choose a Whisper model.
        'model': "large",
        'translate': False,
        'temperature': 0,
        'suppress_tokens': "-1",
        'condition_on_previous_text': True,
        'temperature_increment_on_fallback': 0.2,
        'compression_ratio_threshold': 2.4,
        'logprob_threshold': -1,
        'no_speech_threshold': 0.6,
    }

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
    output = version.predict(**inputs)
    return output['segments'][0]['text']

