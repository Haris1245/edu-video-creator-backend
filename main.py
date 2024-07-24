import g4f
import json
from g4f.Provider import Replicate
topic = input("What topic do you want to make a video about: ")

prompt = f"""
Provide a JSON response with an array named 'script' that includes various types of content. 
The array should contain:
1. An introductory text explaining the {topic} in Bulgarian.Go deep in the subject talk a lot. This is a script for an educational video!
2. At least three examples, each with a type of 'text' and 'equation'.Before the examples start say that the exampels are startingasa a text tag
3. A conclusion summarizing the topic.

Example structure:
{{
    "script": [
        {{"type": "text", "content": "Introduction to the topic."}},
        {{"type": "example", "content": [
            {{"type": "text", "content": "Example 1 text."}},
            {{"type": "equation", "content": "Example 1 equation."}}
        ]}},
        {{"type": "text", "content": "Conclusion text."}}
    ]
}}
"""

response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
).lstrip("```json\n").rstrip("\n```")
print(response)
text = ""
response = json.loads(response)
for i in response['script']:
    if i['type'] == 'text':
        text = text + i['content']
    elif i['type'] == 'example':
        for j in i['content']:
            if j['type'] == 'text':
                text = text + j['content']
print(text)