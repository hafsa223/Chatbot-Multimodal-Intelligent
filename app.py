import streamlit as st
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
import tempfile

from core.command_parser import CommandParser
from core.session_manager import SessionManager

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Multimodal Intelligent Chatbot",
    page_icon="🤖",
    layout="wide"
)

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

# App title
st.title("Multimodal Intelligent Chatbot")

# Sidebar with instructions
with st.sidebar:
    st.header("Commands")
    st.markdown("""
    - **/image [prompt]** - Generate an image
    - **/internet [question]** - Search the web
    - **Upload an image** - Analyze the image
    - **Upload a PDF** - Extract and summarize content
    - **Record audio** - Voice conversation
    """)
    
    # File uploader for images and PDFs
    uploaded_file = st.file_uploader("Upload an image or PDF", type=["jpg", "jpeg", "png", "pdf"])
    
    # Audio recorder
    #audio_bytes = st.audio_recorder("Record audio", sample_rate=16000)
    
    
    #if audio_bytes:
    #    st.audio(audio_bytes, format="audio/wav")
    #    if st.button("Process Audio"):
    #        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
     #           tmp.write(audio_bytes)
     #           tmp_path = tmp.name
            
      #      with open(tmp_path, "rb") as audio_file:
       #         response = command_parser.audio_processor.process_audio(audio_file)
                
            # Add transcription to chat
          #  st.session_state.messages.append({"role": "user", "content": f"🎤 {response['transcription']}"})
           # st.session_state.messages.append({"role": "assistant", "content": response['response']})
            
            # Clean up temp file
           # os.unlink(tmp_path)
            #st.experimental_rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict) and "type" in message["content"]:
            # Handle different response types
            if message["content"]["type"] == "image":
                st.image(message["content"]["url"], caption=message["content"]["prompt"])
                st.write(f"Image generated based on: {message['content']['prompt']}")
            
            elif message["content"]["type"] == "search_result":
                st.write(message["content"]["summary"])
                st.write("Sources:")
            elif message["content"]["type"] == "text":
                st.write(message["content"]["content"])
                
                if "sources" in message["content"]:
                    for source in message["content"]["sources"]:
                        st.write(f"- {source}")

            
            elif message["content"]["type"] == "image_analysis":
                st.write(message["content"]["description"])
                if message["content"]["text"]:
                    st.write(f"Text detected: {message['content']['text']}")
            
            elif message["content"]["type"] == "pdf_summary":
                st.write(f"Summary of {message['content']['filename']}:")
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
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Analyze Image"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": f"📷 Uploaded an image: {uploaded_file.name}"})
            
            # Process the image
            response = command_parser.image_analyzer.analyze(uploaded_file)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    elif file_type == 'pdf':
        if st.button("Process PDF"):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": f"📄 Uploaded a PDF: {uploaded_file.name}"})
            
            # Process the PDF
            response = command_parser.pdf_processor.process(uploaded_file, user_id=st.session_state.user_id)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Chat input
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process the command
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = command_parser.parse_command(user_input, st.session_state.user_id)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display response
            if isinstance(response, dict) and "type" in response:
                if response["type"] == "image":
                    st.image(response["url"], caption=response["prompt"])
                    st.write(f"Image generated based on: {response['prompt']}")
                
                elif response["type"] == "search_result":
                    st.write(response["summary"])
                    st.write("Sources:")
                    for source in response["sources"]:
                        st.write(f"- {source}")

                elif response["type"] == "text":  
                    st.write(response["content"])

                elif response["type"] == "error":
                    st.error(response["message"])
            else:
                st.write(response)
