import os
import streamlit as st  

import fitz  # PyMuPDF
import chromadb
from api.openai_client import OpenAIClient

class RAGEngine:
    def __init__(self, collection_dir="./chromadb"):
        self.client = chromadb.PersistentClient(path=collection_dir)
        self.openai = OpenAIClient()

    def process_pdf(self, pdf_file, collection_name):
        os.makedirs("uploaded", exist_ok=True)
        pdf_path = os.path.join("uploaded", pdf_file.name)

        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        try:
            # Extraction texte avec PyMuPDF
            doc = fitz.open(pdf_path)
            chunks = [page.get_text() for page in doc if page.get_text().strip() != ""]
            doc.close()
        except Exception as e:
            return {"type": "error", "message": f"Erreur extraction texte : {str(e)}"}

        try:
            collection = self.client.get_or_create_collection(collection_name)
            ids = [f"{pdf_file.name}_{i}" for i in range(len(chunks))]
            collection.add(documents=chunks, ids=ids)
            st.write(f"✅ Collection '{collection_name}' ajoutée avec {len(chunks)} chunks.")


        except Exception as e:
            return {"type": "error", "message": f"Erreur ajout dans Chroma : {str(e)}"}

        return {"type": "pdf_summary", "filename": pdf_file.name, "summary": "Document indexé avec succès pour RAG."}

    def ask(self, query, collection_name="default"):
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.query(query_texts=[query], n_results=3)
            docs = results["documents"][0]
        except Exception as e:
            return {"type": "error", "message": f"Erreur RAG : {str(e)}"}

        context = "\n\n".join(docs)
        prompt = f"Voici des extraits d'un document :\n{context}\n\nRéponds à la question suivante : {query}"

        try:
            response = self.openai.generate_response(prompt)
            print("✅ Réponse OpenAI :", response)

        except Exception as e:
            return {"type": "error", "message": f"Erreur appel OpenAI : {str(e)}"}
        print("✅ Prompt envoyé à OpenAI :\n", prompt)
        print("🧠 CONTEXTE (docs extraits) :\n", context)

        return {"type": "text", "content": response}
