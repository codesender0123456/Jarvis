import speech_recognition as sr
import numpy as np
import os
import logging
from threading import Thread, Event
import time

class WakeWordDetector:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = os.getenv('WAKE_WORD', 'hey jarvis').lower()
        self.is_listening = False
        self.stop_listening = Event()
        self.logger = logging.getLogger(__name__)
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        self.logger.info(f"Wake word detector initialized with wake word: '{self.wake_word}'")
    
    def detect_wake_word(self, audio_data):
        """
        Detect wake word in audio data
        """
        try:
            # Convert audio data to text
            text = self.recognizer.recognize_google(audio_data).lower()
            
            # Check if wake word is in the text
            if self.wake_word in text:
                self.logger.info(f"Wake word detected: '{text}'")
                return True
            
            return False
        
        except sr.UnknownValueError:
            # Speech was unintelligible
            return False
        except sr.RequestError as e:
            self.logger.error(f"Could not request results from speech recognition service: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error in wake word detection: {e}")
            return False
    
    def listen_for_wake_word(self, callback=None):
        """
        Continuously listen for wake word
        """
        self.is_listening = True
        self.stop_listening.clear()
        
        def listen_loop():
            while not self.stop_listening.is_set():
                try:
                    with self.microphone as source:
                        self.logger.debug("Listening for wake word...")
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        if self.detect_wake_word(audio):
                            if callback:
                                callback(audio)
                            else:
                                self.logger.info("Wake word detected!")
                
                except sr.WaitTimeoutError:
                    # Timeout, continue listening
                    continue
                except Exception as e:
                    self.logger.error(f"Error in wake word listening loop: {e}")
                    time.sleep(0.1)
        
        # Start listening in a separate thread
        self.listen_thread = Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening_for_wake_word(self):
        """
        Stop listening for wake word
        """
        self.is_listening = False
        self.stop_listening.set()
        if hasattr(self, 'listen_thread'):
            self.listen_thread.join(timeout=1)
    
    def is_wake_word_present(self, text):
        """
        Check if wake word is present in text
        """
        return self.wake_word in text.lower()
    
    def set_wake_word(self, new_wake_word):
        """
        Change the wake word
        """
        self.wake_word = new_wake_word.lower()
        self.logger.info(f"Wake word changed to: '{self.wake_word}'") 