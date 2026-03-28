import streamlit as st
from ingestion import PDFIngestor
from app_graph import PdfChat
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chat with your PDF", page_icon="🤖")
st.markdown("# 📄 Chat with Your PDF")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey! Upload a PDF and ask me questions about it 📚"}]
    st.session_state.app = None
    st.session_state.pdf_loaded = False

# Get GROQ API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

with st.sidebar:
    st.info("🤖 This app uses GROQ API (unlimited free tier).\nYour data is private and secure.")
    
    if not groq_api_key or not groq_api_key.startswith("gsk_"):
        st.error("❌ GROQ_API_KEY not found or invalid in .env file!")
        st.warning("Steps to fix:")
        st.write("""
        1. Go to: https://console.groq.com/keys
        2. Get your API key
        3. Add to .env file:
           GROQ_API_KEY=your_key_here
        """)
        chat_active = True
    else:
        st.success("✅ GROQ API Key loaded!")
        chat_active = False
    
    st.divider()
    
    pdf_files = st.file_uploader(
        "Upload PDFs", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Upload one or more PDF files to chat with"
    )

def initialize_ingestor(pdf_files):
    """Initialize the chatbot with uploaded PDFs"""
    if not pdf_files:
        st.error("❌ Please upload at least one PDF file!")
        return None
    
    try:
        with st.spinner("📚 Processing PDFs... This may take a minute..."):
            try:
                # Create PDF ingestor
                ingestor = PDFIngestor(pdfs=pdf_files, api_key=groq_api_key)
                retriever = ingestor.get_retriever()
                st.success("✅ PDFs uploaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading PDFs: {str(e)[:100]}")
                return None
            
            try:
                # Create chat app
                app = PdfChat(groq_api_key, retriever).graph
                st.success("✅ ChatBot initialized!")
                st.balloons()
                return app
            except Exception as e:
                st.error(f"❌ Error initializing chatbot: {str(e)[:100]}")
                return None
                
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)[:100]}")
        return None

# Initialize button
with st.sidebar:
    if st.button("🚀 Initialize ChatBot", type="primary", disabled=chat_active or not pdf_files):
        st.session_state.app = initialize_ingestor(pdf_files)
        if st.session_state.app:
            st.session_state.pdf_loaded = True

# Main chat interface
st.divider()

app = st.session_state.app

def generate_response(question):
    """Generate response from the chatbot"""
    try:
        result = app.invoke(input={"question": question})
        response = result.get("response", "No response generated")
        return response
    except Exception as e:
        return f"⚠️ Error: {str(e)[:100]}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input(
    placeholder="Ask a question about your PDF...", 
    disabled=chat_active or app is None
):
    if app is None:
        st.error("❌ Please initialize the ChatBot first!")
    else:
        # Add user message
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            response = generate_response(question)
        
        # Add assistant message
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})




