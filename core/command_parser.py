from services.image_generator import ImageGenerator
from services.web_search import WebSearch
from services.image_analyzer import ImageAnalyzer
from services.pdf_processor import PDFProcessor
from services.audio_processor import AudioProcessor
from services.pdf_summary import PDFSummary  # Nouvelle classe pour la gestion des résumés PDF
from services.search_client import SearchClient  # Pour gérer la recherche et résumé du web

class CommandParser:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.image_generator = ImageGenerator()
        self.web_search = WebSearch()
        self.image_analyzer = ImageAnalyzer()
        self.pdf_processor = PDFProcessor()
        self.audio_processor = AudioProcessor()
        self.pdf_summary = PDFSummary()  # Initialisation de la classe de résumé PDF
        self.search_client = SearchClient()  # Initialisation du client de recherche
        
    def parse_command(self, user_input, user_id, file=None):
        """Parse user input and route to appropriate service"""
        
        # Handle image generation command
        if user_input.startswith("/image "):
            prompt = user_input[7:].strip()
            return self.image_generator.generate(prompt)
            
        # Handle web search command
        elif user_input.startswith("/internet "):
            query = user_input[10:].strip()
            search_results = self.search_client.search(query)
            return self.search_client.summarize(search_results, query)
            
        # Handle file uploads
        elif file is not None:
            file_type = file.filename.split('.')[-1].lower()
            
            # Image analysis
            if file_type in ['jpg', 'jpeg', 'png', 'gif']:
                return self.image_analyzer.analyze(file)
                
            # PDF processing
            elif file_type == 'pdf':
                # Process the PDF file to extract text and return a summary
                pdf_text = self.pdf_processor.process(file)
                summary = self.pdf_summary.summarize(pdf_text)
                return summary
                
        # Handle audio input (assuming audio is processed separately)
        elif user_input.startswith("/audio"):
            # This would be triggered by the UI when audio is recorded
            return "Audio processing is handled through the UI"
            
        # Default conversation
        else:
            return f"I'm not sure how to process: {user_input}. Try using a command like /image or /internet."
