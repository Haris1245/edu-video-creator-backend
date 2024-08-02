import assemblyai as aai

class Transcriber:
    def __init__(self, api_key):
        aai.settings.api_key = api_key
        transcription_config = aai.TranscriptionConfig(
            language_code="bg",
            speech_model=aai.SpeechModel.nano
        )
        self.transcriber = aai.Transcriber(config=transcription_config)

    def transcribe(self, audio_url):
        return self.transcriber.transcribe(audio_url)