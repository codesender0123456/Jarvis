# 🚀 Jarvis AI Assistant - Setup Guide

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

### Required Software
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### API Keys
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## 🛠️ Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Jarvis
```

### 2. Quick Setup (Windows)
If you're on Windows, you can use the automated setup:
```bash
setup.bat
```

### 3. Manual Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
copy env_example.txt .env
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 4. Configuration

#### Environment Variables
Edit `backend/.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
WAKE_WORD=hey jarvis
TTS_ENGINE=pyttsx3
DEBUG=True
PORT=5000
```

## 🚀 Running the Application

### Quick Start (Windows)
```bash
start.bat
```

### Manual Start

#### Terminal 1 - Backend
```bash
cd backend
python app.py
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 🎯 Using Jarvis

### Voice Commands
1. **Wake Jarvis**: Say "Hey Jarvis" clearly
2. **Give Commands**: Speak naturally after wake word
3. **Examples**:
   - "What's the weather today?"
   - "Tell me a joke"
   - "What time is it?"
   - "Search for Python tutorials"
   - "Open Google"

### Text Chat
- Use the chat interface for text-based communication
- Type your questions or commands
- Press Enter or click Send

### Manual Microphone Control
- Click the microphone button to start listening
- Click again to stop

## 🔧 Troubleshooting

### Common Issues

#### 1. Microphone Not Working
- **Solution**: Check browser permissions
- **Steps**: 
  1. Click the lock icon in your browser's address bar
  2. Allow microphone access
  3. Refresh the page

#### 2. Wake Word Not Detected
- **Solution**: Speak clearly and check microphone
- **Tips**:
  - Say "Hey Jarvis" slowly and clearly
  - Ensure microphone is working
  - Check for background noise

#### 3. OpenAI API Errors
- **Solution**: Verify API key
- **Steps**:
  1. Check your API key in `backend/.env`
  2. Ensure you have credits in your OpenAI account
  3. Verify the API key is correct

#### 4. Port Already in Use
- **Solution**: Change ports or kill existing processes
- **Steps**:
  1. Change `PORT=5000` to `PORT=5001` in `.env`
  2. Or kill processes using the ports

#### 5. Dependencies Installation Issues
- **Solution**: Update pip and try again
- **Steps**:
  ```bash
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Debug Mode
Enable debug logging by setting `DEBUG=True` in your `.env` file.

## 📁 Project Structure

```
Jarvis/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── speech/             # Speech processing modules
│   │   ├── wake_word.py    # Wake word detection
│   │   ├── speech_to_text.py # Speech-to-text conversion
│   │   └── text_to_speech.py # Text-to-speech conversion
│   ├── ai/                 # AI and NLP modules
│   │   └── assistant.py    # Main AI assistant logic
│   ├── utils/              # Utility functions
│   │   └── logger.py       # Logging configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # React.js frontend
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── App.js          # Main application
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
├── start.bat              # Windows startup script
├── setup.bat              # Windows setup script
└── README.md              # Project documentation
```

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

### Logs
- Backend logs: `backend/logs/`
- Frontend logs: Browser console

## 🚀 Deployment

### Local Development
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

### Production Deployment
1. **Backend**: Deploy to Heroku, AWS, or VPS
2. **Frontend**: Build and deploy to Netlify, Vercel, or static hosting
3. **HTTPS**: Required for microphone access in production

### Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in `backend/logs/`
3. Check browser console for frontend errors
4. Ensure all dependencies are installed correctly

## 🎉 Success!

Once everything is running:
- You should see the Jarvis interface at http://localhost:3000
- The backend API will be available at http://localhost:5000
- Try saying "Hey Jarvis" to test wake word detection
- Use the chat interface for text-based communication

Enjoy your AI assistant! 🤖✨ 