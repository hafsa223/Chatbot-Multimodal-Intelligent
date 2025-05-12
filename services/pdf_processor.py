import os
import re

import streamlit as st  
import fitz  # PyMuPDF
from api.openai_client import OpenAIClient
from services.rag_engine import RAGEngine  # ⬅️ pour l'indexation RAG

class PDFProcessor:
    def __init__(self, session_manager=None):
        self.openai_client = OpenAIClient()
        self.session_manager = session_manager  # Injecté depuis CommandParser

    def process(self, uploaded_file, user_id=None):
        os.makedirs("uploaded", exist_ok=True)
        pdf_path = os.path.join("uploaded", uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            doc = fitz.open(pdf_path)
            full_text = "\n".join([page.get_text() for page in doc])
            doc.close()
        except Exception as e:
            return {"type": "error", "message": f"Erreur PyMuPDF : {str(e)}"}

        try:
            summary = self.openai_client.generate_response(
                f"Voici le contenu extrait d’un PDF :\n\n{full_text}\n\nFais un résumé structuré en français."
            )
        except Exception as e:
            return {"type": "error", "message": f"Erreur OpenAI : {str(e)}"}
        
        #print(f"✅ Collection '{collection_name}' ajoutée avec {len(chunks)} chunks.")


        # 🧠 Indexer dans Chroma pour le RAG
        try:
            rag = RAGEngine()
            collection_name = re.sub(r'\W+', '_', uploaded_file.name.replace(".pdf", ""))
            rag_result = rag.process_pdf(uploaded_file, collection_name)
            if rag_result.get("type") == "error":
                st.warning(f"⚠️ Indexation RAG échouée : {rag_result['message']}")
        except Exception as e:
            st.warning(f"⚠️ Erreur inattendue pendant l'indexation RAG : {str(e)}")

        # 🧠 Enregistrer dans la session
        if self.session_manager and user_id:
            if user_id in self.session_manager.sessions:
                self.session_manager.sessions[user_id]["last_file"] = uploaded_file
                st.write(f"✅ DEBUG - PDF enregistré pour l'utilisateur : {user_id}")
                st.write(f"✅ DEBUG - Fichier : {uploaded_file.name}")

        return {
            "type": "pdf_summary",
            "filename": uploaded_file.name,
            "summary": summary
        }
