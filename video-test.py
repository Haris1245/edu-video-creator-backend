from moviepy.editor import *
import os
import json
import replicate
from dotenv import load_dotenv
import assemblyai as aai
from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
from moviepy.config import change_settings
from moviepy.audio.fx.volumex import volumex
import textwrap
import edge_tts
import asyncio
from bing_image_downloader import downloader
# Configure ImageMagick path
change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/magick"})  # Adjust the path if needed

# Load environment variables
load_dotenv()

# Set up AssemblyAI and ElevenLabs API keys
aai.settings.api_key = "520969975c1f4e34b723af013a097182"


topic = input("What topic do you want to make a video about: ")

# Configure AssemblyAI transcription
transcription_config = aai.TranscriptionConfig(
    language_code="bg",
    speech_model=aai.SpeechModel.nano,
    speech_threshold=0.1
)
transcriber = aai.Transcriber(config=transcription_config)

prompt = f"""
Provide a JSON response with an array named 'script' that includes various types of content. 
        The array should contain:
        1. An introductory text explaining the {topic} in Bulgarian. Go deep into the subject and provide a thorough explanation. This is a script for an educational video!
        2. Each text segment should have an image query that i will use to get an image to display with the text
3. At least 5 text segments
4.Make it that everybody would understand
        Example structure:
        {{
            "script": [
 {{"type": "intro", "content": "intro to the video"}}
                {{"type": "text", "content": "Text about the topic", 'image-query': "a query to find the most descriptive image to show"}},
 {{"type": "text", "content": "Text about the topic", 'image-query': "a query to find the most descriptive image to show"}},
 {{"type": "conclusion", "content": "conclusion to the video"}}           
            ]
        }}
"""

settings = {
    "prompt": prompt,
    'max_tokens': 3024,
    'system_prompt': "You are an educational JSON script writer for videos. Provide JSON only, without additional text."
}
response = replicate.run(
    "meta/meta-llama-3.1-405b-instruct",
    input=settings
)
response_text = "".join(response).lstrip("```").rstrip("```")
response_data = json.loads(response_text)

lessons = []
intro = ""
conclusion = ""
for i in response_data['script']:
    if i['type'] == 'intro':
        intro = i['content']
    elif i['type'] == 'text':
        lessons.append({'text': i['content'], 'query': i['image-query']})
    elif i['type'] == 'conclusion':
        conclusion = i['content']

print(lessons)

bg_path = "/Users/haris/Desktop/edu-video-creator-backend/math-videos/assets/background1.jpg"
bg_clip = ImageClip(bg_path).resize(width=1920)
async def generate_text_audio(text, name):
    tts = edge_tts.Communicate(text, voice="bg-BG-KalinaNeural")
    await tts.save(f'{name}.mp3')

def download_image(query):
    downloader.download(query, limit=1, output_dir='images')

def get_subtitles(audio_url):
    transcript = transcriber.transcribe(audio_url)
    words = [{"word": word.text, "start": word.start / 1000, "end": word.end / 1000} for word in transcript.words]
    return {'text': transcript.text, 'timestamps': words}

def generate_subtitles_clip(subs, delay=0.05):
    text = subs['text']
    timestamps = subs['timestamps']
    
    clips = [((word_info['start'] + delay, word_info['end'] + delay), word_info['word'].upper()) for word_info in timestamps]
    return SubtitlesClip(clips, lambda txt: TextClip(
        txt, fontsize=200, color="white", method='caption', stroke_color="black", stroke_width=6, font="Beyne-Regular"
    )).set_position('center', 'center')

def generate_intro_clip():
    asyncio.run(generate_text_audio(intro, 'introduction'))
    subs = get_subtitles('introduction.mp3')
    subs_clips = generate_subtitles_clip(subs)
    
    bg_clip_with_duration = bg_clip.set_duration(subs_clips.duration)
    
    final_clip = CompositeVideoClip([bg_clip_with_duration, subs_clips], size=(1920, 1080))
    final_clip = final_clip.set_audio(AudioFileClip('introduction.mp3'))
    
    return final_clip

def generate_lesson_sections(lesson, query):
    download_image(query)
    lesson_clip = TextClip(lesson, fontsize=200, color="white", method='caption', stroke_color="black", stroke_width=6, font="Beyne-Regular").set_position('center', 'center')

final_clip = generate_intro_clip()
final_clip.write_videofile('intro.mp4', fps=16)


