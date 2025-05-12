import tempfile
import os
import requests
import openai
from api.openai_client import OpenAIClient

class AudioProcessor:
    def __init__(self):
        self.openai_client = OpenAIClient()
        
    def process_audio(self, audio_file):
        """Transcribe audio and generate response"""
        try:
            # Transcribe the audio using OpenAI's Whisper API
            transcription = self.openai_client.transcribe_audio(audio_file)
            
            # Generate a response to the transcribed text
            response = self.openai_client.generate_response(
                transcription,
                system_prompt="Tu es EduBot, un assistant éducatif intelligent. Tu aides les étudiants à comprendre des concepts, à réviser et à apprendre efficacement. Donne des explications claires, concises et pédagogiques."
            )
            
            return {
                "transcription": transcription,
                "response": response
            }
        except Exception as e:
            return {
                "transcription": f"Erreur de transcription: {str(e)}",
                "response": "Je n'ai pas pu comprendre l'audio. Pourriez-vous réessayer ou reformuler votre question par écrit?"
            }
