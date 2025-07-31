from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import logging
from dotenv import load_dotenv

# Import our modules
from speech.wake_word import WakeWordDetector
from speech.speech_to_text import SpeechToText
from speech.text_to_speech import TextToSpeech
from ai.assistant import AIAssistant
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'jarvis-secret-key')
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize components
wake_detector = WakeWordDetector()
speech_to_text = SpeechToText()
text_to_speech = TextToSpeech()
ai_assistant = AIAssistant()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "message": "Jarvis AI Assistant is running",
        "version": "1.0.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text-based chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get AI response
        ai_response = ai_assistant.get_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text_endpoint():
    """Handle speech-to-text conversion"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        text = speech_to_text.convert_audio_to_text(audio_file)
        
        return jsonify({
            "text": text,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Error in speech-to-text endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech_endpoint():
    """Handle text-to-speech conversion"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        audio_data = text_to_speech.convert_text_to_speech(text)
        
        return jsonify({
            "audio": audio_data,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Error in text-to-speech endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('status', {'message': 'Connected to Jarvis AI Assistant'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

@socketio.on('voice_command')
def handle_voice_command(data):
    """Handle real-time voice commands via WebSocket"""
    try:
        audio_data = data.get('audio')
        if not audio_data:
            emit('error', {'message': 'No audio data received'})
            return
        
        # Convert speech to text
        text = speech_to_text.convert_audio_data_to_text(audio_data)
        
        if text:
            # Get AI response
            ai_response = ai_assistant.get_response(text)
            
            # Convert response to speech
            audio_response = text_to_speech.convert_text_to_speech(ai_response)
            
            emit('ai_response', {
                'text': ai_response,
                'audio': audio_response
            })
        else:
            emit('error', {'message': 'Could not understand speech'})
    
    except Exception as e:
        logger.error(f"Error handling voice command: {str(e)}")
        emit('error', {'message': 'Internal server error'})

@socketio.on('wake_word_detected')
def handle_wake_word():
    """Handle wake word detection"""
    logger.info("Wake word detected")
    emit('wake_word_ack', {'message': 'Jarvis is listening...'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Jarvis AI Assistant on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug) 