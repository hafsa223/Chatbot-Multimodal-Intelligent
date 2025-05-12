import os
import openai
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Set the API key for the openai module
        openai.api_key = self.api_key
        
        # Try to initialize the client with the new API
        try:
            self.client = OpenAI(api_key=self.api_key)
            self.use_new_api = True
        except (TypeError, AttributeError):
            # Fall back to the old API
            self.use_new_api = False
        
    def generate_image(self, prompt):
        """Generate an image using DALL-E"""
        try:
            if self.use_new_api:
                response = self.client.images.generate(
                    model="dall-e-2",
                    prompt=prompt,
                    size="512x512",
                    n=1
                )
                return response.data[0].url
            else:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                return response['data'][0]['url']
        except Exception as e:
            # Return a placeholder if the API call fails
            return {
                "type": "image",
                "url": "https://via.placeholder.com/512x512.png?text=Image+Generation+Failed",
                "prompt": prompt
            }
        
    def generate_response(self, text, system_prompt="You are a helpful assistant."):
        """Generate a response to user text with a specific system prompt"""
        try:
            if self.use_new_api:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=500
                )
                return response.choices[0].message.content
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=500
                )
                return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    def transcribe_audio(self, audio_file):
        """Transcribe audio using Whisper API"""
        try:
            if self.use_new_api:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="fr"
                )
                return response.text
            else:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="fr"
                )
                return response['text']
        except Exception as e:
            return f"Transcription error: {str(e)}"
