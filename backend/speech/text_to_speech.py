import pyttsx3
import gtts
import os
import logging
import tempfile
import base64
from io import BytesIO
import requests

class TextToSpeech:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = os.getenv('TTS_ENGINE', 'pyttsx3')
        self.voice_rate = int(os.getenv('VOICE_RATE', 150))
        self.voice_volume = float(os.getenv('VOICE_VOLUME', 0.9))
        
        # Initialize pyttsx3 engine
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_engine.setProperty('rate', self.voice_rate)
            self.pyttsx3_engine.setProperty('volume', self.voice_volume)
            
            # Get available voices
            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                # Try to set a male voice (usually index 0)
                self.pyttsx3_engine.setProperty('voice', voices[0].id)
            
            self.logger.info("pyttsx3 engine initialized successfully")
        except Exception as e:
            self.logger.warning(f"Could not initialize pyttsx3: {e}")
            self.pyttsx3_engine = None
        
        self.logger.info("Text-to-speech module initialized")
    
    def convert_text_to_speech(self, text, engine=None):
        """
        Convert text to speech using specified engine
        """
        if not text:
            return None
        
        engine = engine or self.engine
        
        try:
            if engine == 'pyttsx3':
                return self._pyttsx3_synthesis(text)
            elif engine == 'gtts':
                return self._gtts_synthesis(text)
            elif engine == 'elevenlabs':
                return self._elevenlabs_synthesis(text)
            else:
                # Fallback to pyttsx3
                return self._pyttsx3_synthesis(text)
        
        except Exception as e:
            self.logger.error(f"Error in text-to-speech conversion: {e}")
            return None
    
    def speak_text(self, text, engine=None):
        """
        Convert text to speech and play it immediately
        """
        try:
            if engine == 'pyttsx3' or engine is None:
                if self.pyttsx3_engine:
                    self.pyttsx3_engine.say(text)
                    self.pyttsx3_engine.runAndWait()
                    return True
                else:
                    # Fallback to gTTS
                    return self._gtts_speak(text)
            else:
                return self._gtts_speak(text)
        
        except Exception as e:
            self.logger.error(f"Error speaking text: {e}")
            return False
    
    def _pyttsx3_synthesis(self, text):
        """
        Use pyttsx3 for text-to-speech
        """
        try:
            if self.pyttsx3_engine is None:
                return None
            
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            # Save speech to file
            self.pyttsx3_engine.save_to_file(text, temp_file_path)
            self.pyttsx3_engine.runAndWait()
            
            # Read the audio file and convert to base64
            with open(temp_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Convert to base64 for web transmission
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            self.logger.info(f"pyttsx3 synthesis completed for text: {text[:50]}...")
            return audio_base64
        
        except Exception as e:
            self.logger.error(f"Error in pyttsx3 synthesis: {e}")
            return None
    
    def _gtts_synthesis(self, text):
        """
        Use Google Text-to-Speech (gTTS)
        """
        try:
            # Create gTTS object
            tts = gtts.gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            tts.save(temp_file_path)
            
            # Read the audio file and convert to base64
            with open(temp_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Convert to base64 for web transmission
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            self.logger.info(f"gTTS synthesis completed for text: {text[:50]}...")
            return audio_base64
        
        except Exception as e:
            self.logger.error(f"Error in gTTS synthesis: {e}")
            return None
    
    def _gtts_speak(self, text):
        """
        Use gTTS to speak text immediately
        """
        try:
            import pygame
            import tempfile
            
            # Create gTTS object
            tts = gtts.gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            tts.save(temp_file_path)
            
            # Play audio using pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.quit()
            os.unlink(temp_file_path)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error in gTTS speak: {e}")
            return False
    
    def _elevenlabs_synthesis(self, text):
        """
        Use ElevenLabs for high-quality text-to-speech
        """
        try:
            # This would require an ElevenLabs API key
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                self.logger.warning("ElevenLabs API key not found, falling back to gTTS")
                return self._gtts_synthesis(text)
            
            # ElevenLabs API endpoint
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Convert to base64
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                self.logger.info(f"ElevenLabs synthesis completed for text: {text[:50]}...")
                return audio_base64
            else:
                self.logger.error(f"ElevenLabs API error: {response.status_code}")
                return self._gtts_synthesis(text)
        
        except Exception as e:
            self.logger.error(f"Error in ElevenLabs synthesis: {e}")
            return self._gtts_synthesis(text)
    
    def get_available_engines(self):
        """
        Get list of available TTS engines
        """
        engines = []
        
        if self.pyttsx3_engine:
            engines.append("pyttsx3")
        
        engines.append("gtts")
        
        if os.getenv('ELEVENLABS_API_KEY'):
            engines.append("elevenlabs")
        
        return engines
    
    def set_voice_properties(self, rate=None, volume=None, voice_id=None):
        """
        Set voice properties for pyttsx3
        """
        if self.pyttsx3_engine:
            if rate is not None:
                self.pyttsx3_engine.setProperty('rate', rate)
                self.voice_rate = rate
            
            if volume is not None:
                self.pyttsx3_engine.setProperty('volume', volume)
                self.voice_volume = volume
            
            if voice_id is not None:
                self.pyttsx3_engine.setProperty('voice', voice_id) 