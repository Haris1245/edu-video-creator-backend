import json
import replicate
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self, topic):
        self.topic = topic
        self.prompt = f"""
        Provide a JSON response with an array named 'script' that includes various types of content. 
        The array should contain:
        1. An introductory text explaining the {topic} in Bulgarian. Go deep into the subject and provide a thorough explanation. This is a script for an educational video!
        2. Three examples, each with a type of 'text' and 'equation'. Before the examples start, include a text tag indicating that examples are beginning.
        3. A conclusion summarizing the topic.
        4. If you use these symbols: ≥ or ≤, use =< and >= instead.If you use * use x, when you use more complex symbols, use simpler symbols
        5. Ensure the topic is explained in a way that everyone can understand.

        Example structure:
        {{
            "script": [
                {{"type": "text", "content": "Introduction to the topic."}},
                {{"type": "example", "content": [
                    {{"type": "description", "content": "Example 1 text."}},
                    {{"type": "equation", "content": "Example 1 answer on how to solve the exercise."}}
                ]}},
                {{"type": "text-conclusion", "content": "Conclusion text."}}
            ]
        }}
        """
        self.response_data = None

    def get_script(self):
        settings = {
            "prompt": self.prompt,
            'max_tokens': 3024,
            'system_prompt': "You are an educational JSON script writer for videos. Provide JSON only, without additional text."
        }
        response = replicate.run(
            "meta/meta-llama-3.1-405b-instruct",
            input=settings
        )
        response_text = "".join(response).lstrip('```').rstrip('```')
        self.response_data = json.loads(response_text)

    def parse_script(self):
        intro = ""
        examples = []

        for item in self.response_data['script']:
            if item['type'] == 'text':
                intro += item['content']
            elif item['type'] == 'example':
                examples.append(item)

        text_conclusion = next(item['content'] for item in self.response_data['script'] if item['type'] == 'text-conclusion')
        return intro, examples, text_conclusion

