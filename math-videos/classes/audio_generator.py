import edge_tts
class AudioGenerator:
    def __init__(self):
        self.tts = edge_tts

    async def generate_audio(self, text, name):
        tts_instance = self.tts.Communicate(text, voice="bg-BG-KalinaNeural")
        await tts_instance.save(f'/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/{name}.mp3')


