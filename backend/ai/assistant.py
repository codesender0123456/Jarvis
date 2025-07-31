import openai
import google.generativeai as genai
import os
import logging
import json
import requests
from datetime import datetime
import webbrowser
import subprocess
import platform
import asyncio
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

class AIAssistant:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        # Google Gemini Configuration
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Google Search Configuration
        self.google_search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('SEARCH_ENGINE_ID')
        
        # Weather Configuration
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        
        # Initialize APIs
        self._initialize_apis()
        
        # Initialize conversation history
        self.conversation_history = []
        self.max_history = 10
        
        # System prompt for Jarvis personality
        self.system_prompt = """You are Jarvis, an intelligent AI assistant inspired by Iron Man's AI. You are helpful, witty, and efficient. You can:

1. Answer questions and provide information
2. Help with tasks and problem-solving
3. Tell jokes and engage in casual conversation
4. Provide weather information, time, and date
5. Help with web searches and opening applications
6. Assist with coding and technical questions
7. Use Google Gemini for enhanced responses
8. Perform real-time web searches
9. Get current weather data

Keep responses concise but informative. Be friendly and slightly witty, but professional. If you can't perform a specific task, suggest alternatives or explain why.

Current capabilities:
- Web search (Google Search API)
- Weather information (OpenWeather API)
- Enhanced AI responses (OpenAI + Google Gemini)
- Basic system operations
- General knowledge and conversation
- Time and date
- Jokes and entertainment

Remember: You're here to help and make the user's life easier!"""
        
        self.logger.info("AI Assistant initialized with enhanced capabilities")
    
    def _initialize_apis(self):
        """Initialize all API clients"""
        # OpenAI
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.logger.info("OpenAI API configured successfully")
        else:
            self.logger.warning("OpenAI API key not found")
        
        # Google Gemini
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.logger.info("Google Gemini API configured successfully")
        else:
            self.logger.warning("Google Gemini API key not found")
            self.gemini_model = None
        
        # Weather API
        if self.weather_api_key:
            try:
                self.owm = OWM(self.weather_api_key)
                self.weather_mgr = self.owm.weather_manager()
                self.logger.info("OpenWeather API configured successfully")
            except Exception as e:
                self.logger.error(f"Error initializing OpenWeather API: {e}")
                self.weather_mgr = None
        else:
            self.logger.warning("OpenWeather API key not found")
            self.weather_mgr = None
    
    def get_response(self, user_input, context=None):
        """
        Get AI response for user input using multiple AI engines
        """
        try:
            # Check for special commands first
            special_response = self._handle_special_commands(user_input)
            if special_response:
                return special_response
            
            # Try OpenAI first, then Gemini as fallback
            response = None
            
            if self.openai_api_key:
                response = self._get_openai_response(user_input, context)
            
            if not response and self.gemini_model:
                response = self._get_gemini_response(user_input, context)
            
            if not response:
                response = self._get_fallback_response(user_input)
            
            # Update conversation history
            self._update_conversation_history(user_input, response)
            
            return response
        
        except Exception as e:
            self.logger.error(f"Error getting AI response: {e}")
            return "I apologize, but I'm experiencing some technical difficulties. Please try again."
    
    def _handle_special_commands(self, user_input):
        """
        Handle special commands and system operations
        """
        input_lower = user_input.lower()
        
        # Time and date
        if any(word in input_lower for word in ['time', 'what time']):
            return self._get_time()
        
        # Date
        if any(word in input_lower for word in ['date', 'what date', 'today']):
            return self._get_date()
        
        # Weather
        if any(word in input_lower for word in ['weather', 'temperature', 'forecast']):
            return self._get_weather(input_lower)
        
        # Open applications
        if 'open' in input_lower:
            return self._open_application(input_lower)
        
        # Web search
        if any(word in input_lower for word in ['search', 'google', 'find', 'look up']):
            return self._web_search(input_lower)
        
        # Jokes
        if any(word in input_lower for word in ['joke', 'funny', 'humor']):
            return self._tell_joke()
        
        # System information
        if any(word in input_lower for word in ['system', 'computer', 'specs']):
            return self._get_system_info()
        
        return None
    
    def _prepare_messages(self, user_input, context=None):
        """
        Prepare messages for OpenAI API
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        for entry in self.conversation_history[-self.max_history:]:
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["assistant"]})
        
        # Add context if provided
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def _get_openai_response(self, user_input, context=None):
        """
        Get response from OpenAI API
        """
        try:
            messages = self._prepare_messages(user_input, context)
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None
    
    def _get_gemini_response(self, user_input, context=None):
        """
        Get response from Google Gemini API
        """
        try:
            if not self.gemini_model:
                return None
            
            prompt = f"{self.system_prompt}\n\nUser: {user_input}"
            if context:
                prompt += f"\nContext: {context}"
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            self.logger.error(f"Google Gemini API error: {e}")
            return None
    
    def _get_fallback_response(self, user_input):
        """
        Fallback response when AI APIs are not available
        """
        input_lower = user_input.lower()
        
        # Simple keyword-based responses
        if 'hello' in input_lower or 'hi' in input_lower:
            return "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
        
        if 'how are you' in input_lower:
            return "I'm functioning perfectly, thank you for asking! How can I assist you?"
        
        if 'bye' in input_lower or 'goodbye' in input_lower:
            return "Goodbye! Feel free to call me anytime you need assistance."
        
        if 'help' in input_lower:
            return "I can help you with various tasks like checking the time, weather, opening applications, web searches, and answering questions. Just ask!"
        
        return "I understand you said: " + user_input + ". I'm currently in offline mode, but I can still help with basic tasks. Try asking about the time, date, or for a joke!"
    
    def _update_conversation_history(self, user_input, assistant_response):
        """
        Update conversation history
        """
        self.conversation_history.append({
            "user": user_input,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _get_time(self):
        """
        Get current time
        """
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}."
    
    def _get_date(self):
        """
        Get current date
        """
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}."
    
    def _get_weather(self, user_input):
        """
        Get weather information using OpenWeather API
        """
        try:
            if not self.weather_mgr:
                return "I'd be happy to check the weather for you! However, I need your location to provide accurate weather information. You can tell me your city or enable location services."
            
            # Extract location from user input
            location = self._extract_location_from_input(user_input)
            if not location:
                return "Please specify a location. For example: 'What's the weather in New York?' or 'Weather in London'"
            
            # Get weather data
            observation = self.weather_mgr.weather_at_place(location)
            weather = observation.weather
            
            # Format weather information
            temp = weather.temperature('celsius')
            humidity = weather.humidity
            description = weather.detailed_status
            
            weather_info = f"Weather in {location}:\n"
            weather_info += f"• Temperature: {temp['temp']:.1f}°C (feels like {temp['feels_like']:.1f}°C)\n"
            weather_info += f"• Condition: {description.capitalize()}\n"
            weather_info += f"• Humidity: {humidity}%\n"
            weather_info += f"• Min/Max: {temp['temp_min']:.1f}°C / {temp['temp_max']:.1f}°C"
            
            return weather_info
        
        except Exception as e:
            self.logger.error(f"Error getting weather: {e}")
            return "I'm sorry, I couldn't retrieve the weather information. Please try again with a different location."
    
    def _extract_location_from_input(self, user_input):
        """
        Extract location from user input
        """
        # Simple location extraction - can be enhanced with NLP
        words = user_input.split()
        location_keywords = ['in', 'at', 'for']
        
        for i, word in enumerate(words):
            if word.lower() in location_keywords and i + 1 < len(words):
                return ' '.join(words[i + 1:])
        
        return None
    
    def _open_application(self, user_input):
        """
        Open applications based on user input
        """
        try:
            if 'chrome' in user_input or 'browser' in user_input:
                webbrowser.open('https://www.google.com')
                return "Opening Google Chrome for you."
            
            elif 'notepad' in user_input:
                if platform.system() == "Windows":
                    subprocess.Popen(['notepad.exe'])
                else:
                    subprocess.Popen(['gedit'])
                return "Opening Notepad for you."
            
            elif 'calculator' in user_input:
                if platform.system() == "Windows":
                    subprocess.Popen(['calc.exe'])
                else:
                    subprocess.Popen(['gnome-calculator'])
                return "Opening Calculator for you."
            
            elif 'google' in user_input:
                webbrowser.open('https://www.google.com')
                return "Opening Google for you."
            
            else:
                return "I can open Chrome, Notepad, Calculator, or Google. Just specify which one you'd like me to open."
        
        except Exception as e:
            self.logger.error(f"Error opening application: {e}")
            return "I'm sorry, I couldn't open that application. Please try again."
    
    def _web_search(self, user_input):
        """
        Perform web search using Google Search API
        """
        try:
            if not self.google_search_api_key or not self.search_engine_id:
                # Fallback to regular Google search
                return self._fallback_web_search(user_input)
            
            # Extract search query
            search_terms = ['search for', 'search', 'find', 'google', 'look up']
            query = user_input
            
            for term in search_terms:
                if term in user_input:
                    query = user_input.replace(term, '').strip()
                    break
            
            if not query:
                return "What would you like me to search for?"
            
            # Perform Google Search API request
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_search_api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': 5
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and data['items']:
                results = []
                for item in data['items'][:3]:  # Top 3 results
                    results.append(f"• {item['title']}: {item['link']}")
                
                search_results = f"Search results for '{query}':\n" + '\n'.join(results)
                return search_results
            else:
                return f"I couldn't find any results for '{query}'. Try a different search term."
        
        except Exception as e:
            self.logger.error(f"Error performing web search: {e}")
            return self._fallback_web_search(user_input)
    
    def _fallback_web_search(self, user_input):
        """
        Fallback web search using regular Google
        """
        try:
            # Extract search query
            search_terms = ['search for', 'search', 'find', 'google', 'look up']
            query = user_input
            
            for term in search_terms:
                if term in user_input:
                    query = user_input.replace(term, '').strip()
                    break
            
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"I'm searching for '{query}' on Google for you."
            else:
                return "What would you like me to search for?"
        
        except Exception as e:
            self.logger.error(f"Error in fallback web search: {e}")
            return "I'm sorry, I couldn't perform the web search. Please try again."
    
    def _tell_joke(self):
        """
        Tell a joke
        """
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fish wearing a bowtie? So-fish-ticated!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "What do you call a computer that sings? A Dell!"
        ]
        
        import random
        return random.choice(jokes)
    
    def _get_system_info(self):
        """
        Get basic system information
        """
        try:
            import psutil
            
            system_info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "CPU Usage": f"{psutil.cpu_percent()}%",
                "Memory Usage": f"{psutil.virtual_memory().percent}%",
                "Disk Usage": f"{psutil.disk_usage('/').percent}%"
            }
            
            info_str = f"System Information:\n"
            for key, value in system_info.items():
                info_str += f"{key}: {value}\n"
            
            return info_str.strip()
        
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return "I'm sorry, I couldn't retrieve the system information."
    
    def clear_conversation_history(self):
        """
        Clear conversation history
        """
        self.conversation_history = []
        return "Conversation history cleared."
    
    def get_conversation_history(self):
        """
        Get conversation history
        """
        return self.conversation_history 