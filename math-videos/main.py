import asyncio
from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
from classes.script_generator import ScriptGenerator
from classes.subtitle_generator import SubtitleGenerator
from classes.transcription_generator import Transcriber
from classes.audio_generator import AudioGenerator
from classes.video_generator import VideoEditor



def main():
    topic = input("What topic do you want to make a video about: ")
    
    script_gen = ScriptGenerator(topic)
    script_gen.get_script()
    intro, examples, text_conclusion = script_gen.parse_script()

    transcriber = Transcriber("520969975c1f4e34b723af013a097182")
    audio_gen = AudioGenerator()
    subtitle_gen = SubtitleGenerator(transcriber)
    video_editor = VideoEditor('/Users/haris/Desktop/edu-video-creator-backend/math-videos/assets/background.jpg', '/Users/haris/Desktop/edu-video-creator-backend/math-videos/assets/melody.mp3')

    # Generate audio
    intro_audio = '/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/introduction.mp3' if intro else None
    conclusion_audio = '/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/text_conclusion.mp3' if text_conclusion else None
    
    if intro:
        asyncio.run(audio_gen.generate_audio(intro, 'introduction'))
    if text_conclusion:
        asyncio.run(audio_gen.generate_audio(text_conclusion, 'text_conclusion'))


    # Get subtitles
    intro_subs = subtitle_gen.get_subtitles('/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/introduction.mp3')
    conclusion_subs = subtitle_gen.get_subtitles('/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/text_conclusion.mp3')
    intro_sub_clips = subtitle_gen.generate_subtitles_clip(intro_subs)
    conclusion_sub_clips = subtitle_gen.generate_subtitles_clip(conclusion_subs)

    # Setup background clip
    music_clip = AudioFileClip(video_editor.music_path).subclip(30, 60).fx(volumex, 0.3).audio_fadein(2).audio_fadeout(2)
    bg_clip = ImageClip(video_editor.bg_path).resize(width=1920)

    # Generate example clips
    examples_clips = [video_editor.generate_example_clip(example, bg_clip) for example in examples]
    examples_clip = concatenate_videoclips(examples_clips)
    examples_clip.audio = CompositeAudioClip([music_clip])

    # Create intro and conclusion clips
    bg_clip_resized_intro = bg_clip.set_duration(intro_sub_clips.duration)
    bg_clip_resized_conclusion = bg_clip.set_duration(conclusion_sub_clips.duration)
    intro_clip = CompositeVideoClip([bg_clip_resized_intro, intro_sub_clips], size=(1920, 1080))
    intro_clip.audio = AudioFileClip('/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/introduction.mp3')

    conclusion_clip = CompositeVideoClip([bg_clip_resized_conclusion, conclusion_sub_clips], size=(1920, 1080))
    conclusion_clip.audio = AudioFileClip('/Users/haris/Desktop/edu-video-creator-backend/math-videos/temp/text_conclusion.mp3')

    # Finalize video
    video_editor.create_video(intro_clip, examples_clip, conclusion_clip)

    if intro_audio and os.path.exists(intro_audio):
        os.remove(intro_audio)
    if conclusion_audio and os.path.exists(conclusion_audio):
        os.remove(conclusion_audio)

if __name__ == "__main__":
    main()
