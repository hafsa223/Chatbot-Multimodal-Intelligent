import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
import base64
from io import BytesIO

# Set page config - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="EduBot - Assistant Intelligent pour les Études",
    page_icon="📚",
    layout="wide"
)

from core.command_parser import CommandParser
from core.session_manager import SessionManager

# Load environment variables
load_dotenv()

# Initialize session manager and command parser
@st.cache_resource
def initialize_components():
    session_manager = SessionManager()
    command_parser = CommandParser(session_manager)
    return session_manager, command_parser

session_manager, command_parser = initialize_components()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "user_id" not in st.session_state:
    st.session_state.user_id = session_manager.create_session()

# Function to autoplay audio
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# App title and description
st.title("📚 EduBot - Ton Assistant Intelligent pour les Études")
st.markdown("""
EduBot t'aide à apprendre plus efficacement en analysant tes documents de cours, 
en répondant à tes questions et en créant des fiches de révision personnalisées.
""")

# Sidebar with features
with st.sidebar:
    st.header("Fonctionnalités")
    st.markdown("""
    - **Analyse de PDF** - Upload tes cours pour les résumer
    - **Questions sur le contenu** - Pose des questions sur tes documents
    - **Analyse d'images** - Comprend tes schémas et diagrammes
    - **Quiz automatique** - Génère des QCM pour tester tes connaissances
    - **Mode vocal** - Parle avec EduBot et écoute ses réponses
    - **Fiches de révision** - Crée des fiches personnalisées
    """)
    
    # Audio feature section
    st.header("Mode Vocal 🎤")
    
    # Check if audio_input is available in this Streamlit version
    has_audio_input = hasattr(st, 'audio_input')
    
    if has_audio_input:
        # Use audio_input function
        audio_value = st.audio_input("Enregistre un message vocal")
        
        if audio_value:
            st.audio(audio_value)
            if st.button("Traiter l'audio"):
                with st.spinner("Traitement en cours..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                        tmp.write(audio_value.getvalue())
                        tmp_path = tmp.name
                    
                    with open(tmp_path, "rb") as audio_file:
                        response = command_parser.audio_processor.process_audio(audio_file)
                        
                    # Add transcription to chat
                    st.session_state.messages.append({"role": "user", "content": f"🎤 {response['transcription']}"})
                    st.session_state.messages.append({"role": "assistant", "content": response['response']})
                   
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.rerun()
    
    # File uploader for PDFs and images
    st.header("Upload de Documents 📄")
    uploaded_file = st.file_uploader("Upload un PDF ou une image", type=["pdf", "jpg", "jpeg", "png"])

# Check if we need to play audio after a rerun
if "play_audio" in st.session_state and st.session_state.play_audio:
    audio_file = st.session_state.play_audio
    autoplay_audio(audio_file)
    # Display audio player as well
    st.audio(audio_file)
    # Clean up
    os.unlink(audio_file)
    del st.session_state.play_audio

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict) and "type" in message["content"]:
            # Handle different response types
            if message["content"]["type"] == "image":
                st.image(message["content"]["url"], caption=message["content"]["prompt"])
                st.write(f"Image générée basée sur: {message['content']['prompt']}")
            
            elif message["content"]["type"] == "search_result":
                st.write(message["content"]["summary"])
                st.write("Sources:")
                for source in message["content"]["sources"]:
                    st.write(f"- {source}")
            
            elif message["content"]["type"] == "image_analysis":
                st.write(message["content"]["description"])
                if message["content"]["text"]:
                    st.write(f"Texte détecté: {message['content']['text']}")
            
            elif message["content"]["type"] == "pdf_summary":
                st.write(f"Résumé de {message['content']['filename']}:")
                st.write(message["content"]["summary"])
            
            elif message["content"]["type"] == "error":
                st.error(message["content"]["message"])
        else:
            # Regular text message
            st.write(message["content"])

# Process uploaded files
if uploaded_file:
    # Determine file type
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    # Process based on file type
    if file_type in ['jpg', 'jpeg', 'png', 'gif']:
        # Display the uploaded image
        st.image(uploaded_file, caption="Image téléchargée", use_column_width=True)
        if st.button("Analyser l'image"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": f"📷 Image téléchargée: {uploaded_file.name}"})
            
            # Process the image
            response = command_parser.image_analyzer.analyze(uploaded_file)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    elif file_type == 'pdf':
        if st.button("Analyser le PDF"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": f"📄 PDF téléchargé: {uploaded_file.name}"})
            
            # Process the PDF
            response = command_parser.pdf_processor.process(uploaded_file)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Chat input
user_input = st.chat_input("Pose ta question à EduBot...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process the command
    with st.chat_message("assistant"):
        with st.spinner("EduBot réfléchit..."):
            response = command_parser.parse_command(user_input, st.session_state.user_id)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display response
            if isinstance(response, dict) and "type" in response:
                if response["type"] == "image":
                    st.image(response["url"], caption=response["prompt"])
                    st.write(f"Image générée basée sur: {response['prompt']}")
                
                elif response["type"] == "search_result":
                    st.write(response["summary"])
                    st.write("Sources:")
                    for source in response["sources"]:
                        st.write(f"- {source}")
                
                elif response["type"] == "error":
                    st.error(response["message"])
            else:
                st.write(response)
                
