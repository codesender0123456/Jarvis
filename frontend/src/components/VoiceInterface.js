import React from 'react';
import { motion } from 'framer-motion';
import { Mic, MicOff, Volume2 } from 'lucide-react';

const VoiceInterface = ({ 
  isListening, 
  isWakeWordActive, 
  onToggleListening, 
  onWakeWord, 
  status 
}) => {
  const getStatusText = () => {
    if (isWakeWordActive) return "Listening for command...";
    if (isListening) return "Listening...";
    if (status === 'processing') return "Processing...";
    if (status === 'speaking') return "Speaking...";
    return "Click to start listening";
  };

  const getStatusColor = () => {
    if (isWakeWordActive || isListening) return "text-green-400";
    if (status === 'processing') return "text-yellow-400";
    if (status === 'speaking') return "text-blue-400";
    return "text-gray-400";
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Status Text */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className={`text-center ${getStatusColor()}`}
      >
        <p className="text-sm font-medium">{getStatusText()}</p>
        {isWakeWordActive && (
          <p className="text-xs mt-1 text-gray-500">Say your command now</p>
        )}
      </motion.div>

      {/* Main Microphone Button */}
      <motion.button
        onClick={onToggleListening}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 ${
          isListening || isWakeWordActive
            ? 'bg-gradient-to-r from-green-500 to-emerald-600 pulse-glow'
            : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
        }`}
      >
        {isListening || isWakeWordActive ? (
          <MicOff className="w-8 h-8 text-white" />
        ) : (
          <Mic className="w-8 h-8 text-white" />
        )}
        
        {/* Animated rings when listening */}
        {(isListening || isWakeWordActive) && (
          <>
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-green-400"
              animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-green-400"
              animate={{ scale: [1, 1.4, 1], opacity: [1, 0, 1] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
            />
          </>
        )}
      </motion.button>

      {/* Wake Word Button */}
      <motion.button
        onClick={onWakeWord}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        disabled={isListening || isWakeWordActive}
        className={`px-6 py-3 rounded-full text-sm font-medium transition-all duration-200 ${
          isWakeWordActive
            ? 'bg-green-500 text-white'
            : 'bg-white/10 text-white hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed'
        }`}
      >
        {isWakeWordActive ? "Wake Word Active" : "Say 'Hey Jarvis'"}
      </motion.button>

      {/* Voice Level Indicator */}
      {(isListening || isWakeWordActive) && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex items-center space-x-2"
        >
          <Volume2 className="w-4 h-4 text-green-400" />
          <div className="flex space-x-1">
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                className="w-1 h-4 bg-green-400 rounded-full"
                animate={{
                  height: [4, 16, 4],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 1,
                  repeat: Infinity,
                  delay: i * 0.1
                }}
              />
            ))}
          </div>
        </motion.div>
      )}

      {/* Instructions */}
      <div className="text-center text-xs text-gray-400 max-w-xs">
        <p>• Click the microphone to start listening</p>
        <p>• Say "Hey Jarvis" to activate wake word</p>
        <p>• Speak clearly for best results</p>
      </div>
    </div>
  );
};

export default VoiceInterface; 