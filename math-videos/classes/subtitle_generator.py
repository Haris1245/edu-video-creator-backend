from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/magick"})  # Adjust the path if needed

class SubtitleGenerator:
    def __init__(self, transcriber):
        self.transcriber = transcriber

    def get_subtitles(self, audio_url):
        transcript = self.transcriber.transcribe(audio_url)
        words = [{"word": word.text, "start": word.start / 1000, "end": word.end / 1000} for word in transcript.words]
        return {'text': transcript.text, 'timestamps': words}

    def generate_subtitles_clip(self, subs, delay=0.05):
        text = subs['text']
        timestamps = subs['timestamps']
        
        clips = [((word_info['start'] + delay, word_info['end'] + delay), word_info['word'].upper()) for word_info in timestamps]
        return SubtitlesClip(clips, lambda txt: TextClip(
            txt, fontsize=200, color="white", method='caption', stroke_color="black", stroke_width=6, font="Beyne-Regular"
        )).set_position('center', 'center')
