import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Settings, Volume2, VolumeX } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import VoiceInterface from './components/VoiceInterface';
import JarvisAvatar from './components/JarvisAvatar';
import SettingsPanel from './components/SettingsPanel';
import { useSocket } from './hooks/useSocket';
import { useSpeechRecognition } from './hooks/useSpeechRecognition';

function App() {
  const [isListening, setIsListening] = useState(false);
  const [isWakeWordActive, setIsWakeWordActive] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [status, setStatus] = useState('idle'); // idle, listening, processing, speaking

  const socket = useSocket();
  const { startListening, stopListening, transcript } = useSpeechRecognition();

  // Initialize with welcome message
  useEffect(() => {
    setMessages([
      {
        id: 1,
        type: 'assistant',
        text: "Hello! I'm Jarvis, your AI assistant. Say 'Hey Jarvis' to wake me up, or click the microphone to start talking.",
        timestamp: new Date()
      }
    ]);
  }, []);

  // Handle socket events
  useEffect(() => {
    if (!socket) return;

    socket.on('status', (data) => {
      console.log('Status:', data.message);
    });

    socket.on('ai_response', (data) => {
      const newMessage = {
        id: Date.now(),
        type: 'assistant',
        text: data.text,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newMessage]);
      setStatus('speaking');
      
      // Play audio response if available
      if (data.audio && !isMuted) {
        playAudioResponse(data.audio);
      }
    });

    socket.on('wake_word_ack', (data) => {
      setIsWakeWordActive(true);
      setStatus('listening');
      console.log('Wake word acknowledged:', data.message);
    });

    socket.on('error', (data) => {
      console.error('Socket error:', data.message);
      setStatus('idle');
    });

    return () => {
      socket.off('status');
      socket.off('ai_response');
      socket.off('wake_word_ack');
      socket.off('error');
    };
  }, [socket, isMuted]);

  // Handle speech recognition
  useEffect(() => {
    if (transcript && isWakeWordActive) {
      handleVoiceCommand(transcript);
    }
  }, [transcript, isWakeWordActive]);

  const handleVoiceCommand = async (command) => {
    if (!command.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: command,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    // Send to backend
    if (socket) {
      socket.emit('voice_command', { text: command });
      setStatus('processing');
    }

    setIsWakeWordActive(false);
    setStatus('idle');
  };

  const handleTextMessage = async (text) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    // Send to backend
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        const assistantMessage = {
          id: Date.now() + 1,
          type: 'assistant',
          text: data.response,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
      setIsListening(false);
      setStatus('idle');
    } else {
      startListening();
      setIsListening(true);
      setStatus('listening');
    }
  };

  const toggleWakeWord = () => {
    if (socket) {
      socket.emit('wake_word_detected');
    }
  };

  const playAudioResponse = (audioBase64) => {
    try {
      const audioBlob = new Blob([Uint8Array.from(atob(audioBase64), c => c.charCodeAt(0))], { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
        setStatus('idle');
      };
    } catch (error) {
      console.error('Error playing audio:', error);
      setStatus('idle');
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex flex-col">
      {/* Header */}
      <motion.header 
        className="glass p-4 flex justify-between items-center"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-lg">J</span>
          </div>
          <h1 className="text-2xl font-bold gradient-text">Jarvis AI</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleMute}
            className="p-2 rounded-full glass hover:bg-white/20 transition-colors"
            title={isMuted ? "Unmute" : "Mute"}
          >
            {isMuted ? <VolumeX className="w-5 h-5 text-white" /> : <Volume2 className="w-5 h-5 text-white" />}
          </button>
          
          <button
            onClick={() => setIsSettingsOpen(true)}
            className="p-2 rounded-full glass hover:bg-white/20 transition-colors"
            title="Settings"
          >
            <Settings className="w-5 h-5 text-white" />
          </button>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row p-4 gap-4">
        {/* Chat Interface */}
        <motion.div 
          className="flex-1 glass rounded-2xl p-6"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <ChatInterface 
            messages={messages}
            onSendMessage={handleTextMessage}
            status={status}
          />
        </motion.div>

        {/* Voice Interface */}
        <motion.div 
          className="lg:w-96 glass rounded-2xl p-6 flex flex-col items-center justify-center"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <JarvisAvatar status={status} />
          
          <VoiceInterface
            isListening={isListening}
            isWakeWordActive={isWakeWordActive}
            onToggleListening={toggleListening}
            onWakeWord={toggleWakeWord}
            status={status}
          />
        </motion.div>
      </div>

      {/* Settings Panel */}
      <AnimatePresence>
        {isSettingsOpen && (
          <SettingsPanel 
            onClose={() => setIsSettingsOpen(false)}
            isMuted={isMuted}
            onToggleMute={toggleMute}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App; 