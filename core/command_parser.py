from services.visual_aid_generator import ImageGenerator
from services.edu_search import WebSearch
from services.image_analyzer import ImageAnalyzer
from services.pdf_processor import PDFProcessor
from services.audio_processor import AudioProcessor

# Rest of your code...

class CommandParser:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.image_generator = ImageGenerator()
        self.web_search = WebSearch()
        self.image_analyzer = ImageAnalyzer()
        self.pdf_processor = PDFProcessor()
        self.audio_processor = AudioProcessor()
        
    def parse_command(self, user_input, user_id, file=None):
        """Parse user input and route to appropriate service"""
        
        # Educational commands
        if user_input.startswith("/quiz "):
            topic = user_input[6:].strip()
            return f"Voici un quiz sur {topic}:\n\n" + self._generate_quiz(topic)
            
        elif user_input.startswith("/fiche "):
            topic = user_input[7:].strip()
            return f"Voici une fiche de révision sur {topic}:\n\n" + self._generate_study_card(topic)
        
        # Handle image generation command
        elif user_input.startswith("/image "):
            prompt = user_input[7:].strip()
            return self.image_generator.generate(prompt)
            
        # Handle web search command
        elif user_input.startswith("/internet "):
            query = user_input[10:].strip()
            return self.web_search.search(query)
            
        # Handle file uploads
        elif file is not None:
            file_type = file.filename.split('.')[-1].lower()
            
            # Image analysis
            if file_type in ['jpg', 'jpeg', 'png', 'gif']:
                return self.image_analyzer.analyze(file)
                
            # PDF processing
            elif file_type == 'pdf':
                return self.pdf_processor.process(file)
                
        # Default educational assistant response
        else:
            from api.openai_client import OpenAIClient
            openai_client = OpenAIClient()
            return openai_client.generate_response(
                user_input,
                system_prompt="Tu es EduBot, un assistant éducatif intelligent. Tu aides les étudiants à comprendre des concepts, à réviser et à apprendre efficacement. Donne des explications claires, concises et pédagogiques."
            )
    
    def _generate_quiz(self, topic):
        """Generate a quiz on the given topic"""
        from api.openai_client import OpenAIClient
        openai_client = OpenAIClient()
        prompt = f"Crée un quiz de 5 questions à choix multiples sur le sujet: {topic}. Pour chaque question, fournis 4 options et indique la bonne réponse."
        return openai_client.generate_response(prompt)