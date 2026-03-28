# TalkDocs 2.0 - Chat with Your PDF

A modern PDF chat application using GROQ API and LangChain for intelligent document Q&A.

## Features

✨ **Upload & Process PDFs** - Upload multiple PDF files for processing
🤖 **AI-Powered Responses** - Uses GROQ's Llama 3.3 70B model (unlimited free tier)
📚 **Smart Retrieval** - Intelligent routing between document context and general knowledge
💬 **Conversational Interface** - Clean Streamlit UI with chat history
🔒 **Privacy First** - All conversations stay local, no data collection

## Quick Start

### 1. Clone & Setup

```bash
cd "c:\COMMON DISK FILES\github projects\TalkDocs 2.0"

# Create virtual environment (if not exists)
python -m venv .venv

# Activate venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your GROQ API key
# Get free key from: https://console.groq.com
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
TalkDocs 2.0/
├── app.py                 # Main Streamlit application
├── app_graph.py           # LLM logic and RAG workflow
├── ingestion.py           # PDF processing & embeddings
├── router.py              # Query routing logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── .env.example          # Example env file (template)
├── media/                # Images and assets
├── .vscode/              # VS Code configuration
│   ├── settings.json     # Python interpreter & Pylance config
│   └── launch.json       # Debugging configuration
└── README.md             # This file
```

## Requirements

- **Python**: 3.10 or higher
- **GROQ API Key**: Get free from [console.groq.com](https://console.groq.com)
- **Dependencies**: See requirements.txt

## Technology Stack

| Component | Library | Version |
|-----------|---------|---------|
| **UI Framework** | Streamlit | 1.38.0 |
| **LLM** | GROQ ChatGroq | Llama 3.3 70B |
| **Orchestration** | LangGraph | 0.2.28 |
| **NLP Framework** | LangChain | 0.3.1+ |
| **Vector DB** | FAISS | 1.8.0 |
| **PDF Processing** | PyPDF | 5.0.1 |
| **Embeddings** | Custom Hash-based | Pure Python |

## Usage

### Upload PDFs
1. Click **"Upload PDFs"** in the sidebar
2. Select one or more PDF files
3. Click **"Initialize ChatBot"**

### Ask Questions
1. Type your question in the chat input
2. Wait for the AI to process and respond
3. Questions are automatically routed:
   - **Vectorstore Path**: For questions about PDF content
   - **General Path**: For questions requiring general knowledge

### View History
- Chat history is maintained during your session
- Previous messages appear below the input field

## Troubleshooting

### Import Errors in VS Code
If you see "Import could not be resolved" errors in VS Code:

1. **Reload VS Code**: `Ctrl+Shift+P` → "Developer: Reload Window"
2. **Select Python Interpreter**: 
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Choose: `.venv/Scripts/python.exe`
3. **Restart Pylance**: 
   - `Ctrl+Shift+P` → "Pylance: Restart Language Server"

### GROQ API Errors (403)
- ✅ Check your GROQ_API_KEY is correct in `.env`
- ✅ Ensure API key is not expired
- ✅ Check internet connection

### PDF Upload Issues
- ✅ Ensure PDF is valid and not corrupted
- ✅ Try with a smaller PDF first
- ✅ Check disk space available

## Configuration Files

### .vscode/settings.json
Configures VS Code to use the project's virtual environment:
- Sets Python interpreter to `.venv/Scripts/python.exe`
- Enables Pylance type checking
- Configures module resolution paths
- Formats code on save

### .vscode/launch.json
Debugging configurations:
- **Python: Current File** - Debug any Python file
- **Streamlit App** - Debug the Streamlit app

## API Reference

### GROQ (Llama 3.3 70B)
- **Free Tier**: Unlimited requests, no rate limits
- **Model**: llama-3.3-70b-versatile
- **Temperature**: 0 (deterministic responses)
- **Get Key**: [groq.com](https://groq.com)

## Performance Tips

1. **Chunk Size**: Text is split into 200-token chunks (configurable in ingestion.py)
2. **Embeddings**: Uses efficient hash-based method (pure Python)
3. **Retrieval**: MMR search with k=3 documents
4. **Response Time**: 1-3 seconds typical latency

## Limitations

- **Embeddings**: Hash-based embeddings are less accurate than neural models (acceptable trade-off for speed/stability)
- **Memory**: Conversation history per session only (not persisted)
- **PDF Size**: Tested with PDFs up to 100MB
- **Context**: Uses top 3 most relevant document chunks

## Future Enhancements

- [ ] Persist conversation history to database
- [ ] Export chat as PDF report
- [ ] Support for document search history
- [ ] Multi-user sessions
- [ ] Custom system prompts
- [ ] Document metadata extraction
- [ ] Rate limiting and usage tracking

## Development

### Virtual Environment

```bash
# Create
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Install dev packages
pip install -r requirements.txt
```

### Running Tests
```bash
# Test imports
python check_packages.py

# Test system
python test_imports.py
```

### Code Style
- Python 3.10+ (PEP 484)
- Type hints where practical
- Docstrings for functions

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check `.env` has GROQ_API_KEY
2. Run `pip install -r requirements.txt`
3. Restart VS Code
4. Check internet connection

## Credits

Built with:
- **GROQ**: For the amazing free LLM API
- **LangChain**: For the orchestration framework
- **Streamlit**: For the intuitive UI framework
- **FAISS**: For efficient vector search

---

**Status**: ✅ Production Ready
**Last Updated**: March 25, 2026
**Version**: 2.0
