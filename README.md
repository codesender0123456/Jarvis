# 🎯 Jarvis AI Assistant

A complete, web-based AI assistant with speech recognition, natural language processing, and text-to-speech capabilities.

## ✨ Features

- 🎤 **Wake-word Detection**: "Hey Jarvis" activation
- 🗣️ **Speech-to-Text**: Real-time voice command processing
- 🤖 **AI Intelligence**: OpenAI GPT-3.5/4 powered responses
- 🔊 **Text-to-Speech**: Natural voice responses
- 🌐 **Web Interface**: Modern, responsive UI
- 📱 **Cross-platform**: Works on Windows, Mac, Linux
- 🔧 **Modular Design**: Easy to extend and customize

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Microphone access
- OpenAI API key

### Installation

1. **Clone and setup backend:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup frontend:**
```bash
cd frontend
npm install
```

3. **Configure environment:**
```bash
# Copy and edit the environment file
cp backend/.env.example backend/.env
# Add your OpenAI API key to .env
```

4. **Run the application:**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

5. **Access the assistant:**
   - Open http://localhost:3000 in your browser
   - Allow microphone access when prompted
   - Say "Hey Jarvis" to activate

## 📁 Project Structure

```
Jarvis/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── speech/             # Speech processing modules
│   ├── ai/                 # AI and NLP modules
│   ├── utils/              # Utility functions
│   └── requirements.txt    # Python dependencies
├── frontend/               # React.js frontend
│   ├── src/                # Source code
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
└── README.md              # This file
```

## 🎯 Usage

1. **Wake the assistant**: Say "Hey Jarvis" clearly
2. **Give commands**: Ask questions, request tasks, or chat naturally
3. **Examples**:
   - "What's the weather today?"
   - "Tell me a joke"
   - "What time is it?"
   - "Search for Python tutorials"
   - "Open Google"

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `WAKE_WORD`: Custom wake word (default: "hey jarvis")
- `VOICE_MODEL`: TTS voice model selection
- `DEBUG`: Enable debug mode

### Customization
- Modify wake word in `backend/speech/wake_word.py`
- Change AI personality in `backend/ai/assistant.py`
- Customize UI in `frontend/src/components/`

## 🚀 Deployment

### Local Development
- Backend runs on http://localhost:5000
- Frontend runs on http://localhost:3000

### Production Deployment
- Use Docker containers
- Deploy to Heroku, AWS, or VPS
- Configure HTTPS for microphone access

## 🛠️ Troubleshooting

### Common Issues
1. **Microphone not working**: Check browser permissions
2. **Wake word not detected**: Speak clearly, check microphone
3. **API errors**: Verify OpenAI API key
4. **Port conflicts**: Change ports in configuration

### Debug Mode
Enable debug logging by setting `DEBUG=True` in environment variables.

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built with ❤️ using Python, React, and OpenAI** 