
# EduBot 🧠📚 – Assistant Intelligent pour l'Éducation

EduBot est une application NLP interactive développée en Python et Streamlit. Elle agit comme un tuteur virtuel capable d’analyser des documents pédagogiques, de répondre à des questions d’étudiants, de générer des résumés, des QCMs, des supports visuels et même de vocaliser les réponses. 🧑‍🏫🤖

---

## 🎯 Objectif
Fournir un assistant éducatif intelligent basé sur l'IA (OpenAI/Mistral) avec des capacités de recherche RAG, de traitement de documents PDF, d’analyse d’images, d’audio et de génération de contenus pédagogiques.

---

## 🚀 Fonctionnalités principales

- ✅ Upload et analyse de fichiers PDF (cours, sujets d’examens)
- ✅ Résumé de contenu + explications simplifiées
- ✅ Génération de QCM à partir de documents
- ✅ Interrogation en langage naturel (chatbot)
- ✅ Recherche de ressources pédagogiques complémentaires
- ✅ Génération d’aides visuelles (schémas, cartes mentales)
- ✅ Lecture vocale des contenus (text-to-speech)
- ✅ Historique de session (mémoire contextuelle)
- ✅ Moteur RAG avec ChromaDB
- ✅ Interface Streamlit intuitive

---

## 🧱 Architecture du projet

```
├── app.py                    # Interface principale Streamlit
├── config.py                 # Paramètres de configuration
├── requirements.txt          # Dépendances
├── .env                      # Clés API et variables sensibles
├── README.md                 # Ce fichier ✨
├── core/
│   ├── command_parser.py     # Analyse des requêtes utilisateurs
│   └── session_manager.py    # Gestion des sessions utilisateurs
├── services/
│   ├── pdf_processor.py      # Traitement de documents PDF
│   ├── image_generator.py    # Génération d'aides visuelles
│   ├── image_analyzer.py     # Analyse d’images intégrées
│   ├── web_search.py         # Recherche web éducative
│   ├── audio_processor.py    # Synthèse et transcription audio
│   └── rag_engine.py         # Fonctionnalité RAG (base ChromaDB)
├── api/
│   ├── openai_client.py      # Intégration API OpenAI
│   └── stability_client.py   # API Stable Diffusion (visuels)
└── utils/
    ├── file_handler.py       # Upload & gestion fichiers
    └── text_processor.py     # Nettoyage & segmentations de texte
```

---

## 🔧 Installation

```bash
git clone https://github.com/votre-utilisateur/EduBot.git
cd EduBot
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
```

Créer un fichier `.env` :
```
OPENAI_API_KEY=your_openai_key
MISTRAL_API_KEY=your_mistral_key
```

---

## 📌 Lancement

```bash
streamlit run app.py
```

---

## ✍️ Auteurs

- Hafsa Moumni
- Projet encadré à Ynov, Master 1 Data Science

---

## 📎 Déploiement final

- Front hébergé sur **Streamlit Cloud**
- Projet complet sur Github avec TPs + Readme détaillé ✅

---

## 📚 Licence

MIT
