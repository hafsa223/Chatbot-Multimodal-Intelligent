from services.visual_aid_generator import ImageGenerator
from services.edu_search import WebSearch
from services.image_analyzer import ImageAnalyzer
from services.pdf_processor import PDFProcessor
from services.audio_processor import AudioProcessor
from services.rag_engine import RAGEngine

class CommandParser:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.image_generator = ImageGenerator()
        self.web_search = WebSearch()
        self.image_analyzer = ImageAnalyzer()
        self.pdf_processor = PDFProcessor(session_manager=session_manager)
        self.audio_processor = AudioProcessor()
        self.rag_engine = RAGEngine()

    def parse_command(self, user_input, user_id, file=None):
        if user_input.startswith("/image "):
            prompt = user_input[7:].strip()
            return self.image_generator.generate(prompt)

        elif user_input.startswith("/internet "):
            query = user_input[10:].strip()
            return self.web_search.search(query)

        elif user_input.startswith("/askpdf "):
            question = user_input[8:].strip()
            uploaded_pdf = self.session_manager.sessions.get(user_id, {}).get("last_file")
            if uploaded_pdf and uploaded_pdf.name.endswith(".pdf"):
                collection_name = uploaded_pdf.name.replace(".pdf", "")
                response = self.rag_engine.ask(question, collection_name)
                print("✅ Réponse renvoyée par RAG:", response)
                return response
            return {"type": "error", "message": "Aucun PDF n'a encore été traité pour cette session."}

        elif file is not None:
            file_type = file.name.split('.')[-1].lower()
            if file_type in ['jpg', 'jpeg', 'png']:
                return self.image_analyzer.analyze(file)
            elif file_type == 'pdf':
                return self.pdf_processor.process(file, user_id=user_id)

        elif user_input.startswith("/audio"):
            return "Audio processing is handled through the UI"

        else:
            return {
                "type": "text",
                "content": f"Je ne comprends pas cette commande : {user_input}. Essaie /image, /internet ou /askpdf."
            }
