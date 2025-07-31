import speech_recognition as sr
import whisper
import numpy as np
import os
import logging
import tempfile
from io import BytesIO

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger = logging.getLogger(__name__)
        
        # Initialize Whisper model
        try:
            self.whisper_model = whisper.load_model("base")
            self.logger.info("Whisper model loaded successfully")
        except Exception as e:
            self.logger.warning(f"Could not load Whisper model: {e}")
            self.whisper_model = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        self.logger.info("Speech-to-text module initialized")
    
    def convert_audio_to_text(self, audio_file):
        """
        Convert audio file to text using multiple engines
        """
        try:
            # Try Google Speech Recognition first
            text = self._google_speech_recognition(audio_file)
            if text:
                return text
            
            # Fallback to Whisper
            if self.whisper_model:
                text = self._whisper_recognition(audio_file)
                if text:
                    return text
            
            return ""
        
        except Exception as e:
            self.logger.error(f"Error converting audio to text: {e}")
            return ""
    
    def convert_audio_data_to_text(self, audio_data):
        """
        Convert audio data (bytes) to text
        """
        try:
            # Create a temporary file from audio data
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Convert to text
            text = self.convert_audio_to_text(temp_file_path)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            return text
        
        except Exception as e:
            self.logger.error(f"Error converting audio data to text: {e}")
            return ""
    
    def listen_and_convert(self, timeout=5, phrase_time_limit=10):
        """
        Listen to microphone and convert to text
        """
        try:
            with self.microphone as source:
                self.logger.info("Listening for speech...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                # Convert to text
                text = self._google_speech_recognition(audio)
                if not text and self.whisper_model:
                    text = self._whisper_recognition(audio)
                
                return text
        
        except sr.WaitTimeoutError:
            self.logger.info("No speech detected within timeout")
            return ""
        except Exception as e:
            self.logger.error(f"Error in listen_and_convert: {e}")
            return ""
    
    def _google_speech_recognition(self, audio_input):
        """
        Use Google Speech Recognition
        """
        try:
            if isinstance(audio_input, str):
                # Audio file path
                with sr.AudioFile(audio_input) as source:
                    audio = self.recognizer.record(source)
            else:
                # Audio data object
                audio = audio_input
            
            text = self.recognizer.recognize_google(audio)
            self.logger.info(f"Google Speech Recognition result: {text}")
            return text
        
        except sr.UnknownValueError:
            self.logger.debug("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            self.logger.error(f"Could not request results from Google Speech Recognition service: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Error in Google Speech Recognition: {e}")
            return ""
    
    def _whisper_recognition(self, audio_input):
        """
        Use Whisper for speech recognition
        """
        try:
            if self.whisper_model is None:
                return ""
            
            if isinstance(audio_input, str):
                # Audio file path
                result = self.whisper_model.transcribe(audio_input)
            else:
                # Audio data object - save to temp file first
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(audio_input.get_wav_data())
                    temp_file_path = temp_file.name
                
                result = self.whisper_model.transcribe(temp_file_path)
                os.unlink(temp_file_path)
            
            text = result["text"].strip()
            self.logger.info(f"Whisper recognition result: {text}")
            return text
        
        except Exception as e:
            self.logger.error(f"Error in Whisper recognition: {e}")
            return ""
    
    def get_available_engines(self):
        """
        Get list of available speech recognition engines
        """
        engines = ["Google Speech Recognition"]
        if self.whisper_model:
            engines.append("Whisper")
        return engines 