# 🚀 Quick Setup - Jarvis AI Assistant

## ⚡ One-Click Installation

1. **Run the installer:**
   ```bash
   install.bat
   ```

2. **Configure your API keys:**
   Edit `backend/.env` and add your keys:

   ```env
   # OpenAI Configuration (REQUIRED)
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo

   # LiveKit Configuration (for real-time audio/video)
   LIVEKIT_API_KEY=API6UsFYqEXAQrB
   LIVEKIT_API_SECRET=fZISbgNaHMw2mEeXkLrz5rOCswBD8g8kh7jvHWauI7z
   LIVEKIT_URL=wss://jarvis-1hw5rfj0.livekit.cloud

   # Google Gemini API Configuration
   GOOGLE_API_KEY=AIzaSyCAdlB2Jvr-Ykfyee9fVGh4ktjnIqs7cts

   # Google Search API Configuration
   GOOGLE_SEARCH_API_KEY=AIzaSyCAdlB2Jvr-Ykfyee9fVGh4ktjnIqs7cts
   SEARCH_ENGINE_ID=c245279e2fb274ac1

   # Weather API Configuration
   OPENWEATHER_API_KEY=930b855bea48e096a0bfa8c41f9776b1

   # Speech Configuration
   WAKE_WORD=hey jarvis
   SAMPLE_RATE=16000
   CHUNK_SIZE=1024

   # TTS Configuration
   TTS_ENGINE=pyttsx3
   VOICE_RATE=150
   VOICE_VOLUME=0.9

   # Server Configuration
   FLASK_ENV=development
   DEBUG=True
   PORT=5000

   # Audio Configuration
   AUDIO_FORMAT=pyaudio.paInt16
   CHANNELS=1
   ```

3. **Launch Jarvis:**
   ```bash
   start.bat
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000

## 🎯 Enhanced Features with Your APIs

### 🌐 **Google Search Integration**
- Real-time web search results
- Command: "Search for Python tutorials"
- Uses your Google Search API key

### 🌤️ **Weather Information**
- Current weather data for any location
- Command: "What's the weather in New York?"
- Uses your OpenWeather API key

### 🤖 **Google Gemini AI**
- Enhanced AI responses with Google's latest model
- Fallback when OpenAI is unavailable
- Uses your Google Gemini API key

### 🎥 **LiveKit Real-time Communication**
- High-quality audio/video communication
- Real-time voice processing
- Uses your LiveKit credentials

## 🎮 Voice Commands

Try these commands with your enhanced Jarvis:

- **"Hey Jarvis, what's the weather in London?"**
- **"Hey Jarvis, search for machine learning tutorials"**
- **"Hey Jarvis, tell me a joke"**
- **"Hey Jarvis, what time is it?"**
- **"Hey Jarvis, open Google"**

## 🔧 Troubleshooting

### If you get API errors:
1. Check that all API keys are correctly copied
2. Ensure you have credits in your OpenAI account
3. Verify Google Search API is enabled in Google Cloud Console

### If microphone doesn't work:
1. Allow microphone access in your browser
2. Check that your microphone is working
3. Try refreshing the page

### If installation fails:
1. Make sure Python 3.8+ and Node.js 16+ are installed
2. Run `install.bat` again
3. Check the error messages for specific issues

## 📞 Support

Your Jarvis AI Assistant is now ready with:
- ✅ OpenAI GPT integration
- ✅ Google Gemini AI backup
- ✅ Real-time web search
- ✅ Weather information
- ✅ Voice commands
- ✅ Beautiful web interface

Enjoy your enhanced AI assistant! 🤖✨ 