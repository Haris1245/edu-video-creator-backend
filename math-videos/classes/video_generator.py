
import textwrap
from moviepy.editor import *
from moviepy.video.tools.subtitles import  TextClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/magick"})  # Adjust the path if needed

class VideoEditor:
    def __init__(self, bg_path, music_path):
        self.bg_path = bg_path
        self.music_path = music_path
        
    def wrap_text(self, text, width):
        return '\n'.join(textwrap.wrap(text, width=width))

    def generate_example_clip(self, example, bg_clip):
        description_text = self.wrap_text(example['content'][0]['content'], width=40)
        answer_text = self.wrap_text(example['content'][1]['content'], width=40)

        description_clip = TextClip(
            description_text, fontsize=60, color="white", method='label', kerning=-2, interline=-1,
            stroke_color="black", stroke_width=2, font="Beyne-Regular"
        ).set_duration(10).fadein(0.9).fadeout(0.8).set_start(0).set_position((50, 50))

        description_height = description_clip.size[1]

        answer_clip = TextClip(
            f"Отговор: {answer_text}", fontsize=60, color="white", method='label',
            stroke_color="black", stroke_width=2, font="Beyne-Regular"
        ).set_duration(5).set_start(5).fadein(0.8).fadeout(0.8).set_end(10).set_position((50, 50 + description_height + 20))

        return CompositeVideoClip([bg_clip, description_clip, answer_clip], size=(1920, 1080)).set_duration(10)

    def create_video(self, intro_clip, examples_clip, conclusion_clip):
        final_clip = concatenate_videoclips([intro_clip, examples_clip, conclusion_clip])
        final_clip.write_videofile("/Users/haris/Desktop/edu-video-creator-backend/math-videos/output/video1.mp4", fps=16)
