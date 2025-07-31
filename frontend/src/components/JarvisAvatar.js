import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Cpu, Zap } from 'lucide-react';

const JarvisAvatar = ({ status }) => {
  const getAvatarState = () => {
    switch (status) {
      case 'listening':
        return {
          icon: <Bot className="w-12 h-12 text-green-400" />,
          color: 'from-green-500 to-emerald-600',
          animation: 'wave-animation',
          glow: 'shadow-green-400/50'
        };
      case 'processing':
        return {
          icon: <Cpu className="w-12 h-12 text-yellow-400" />,
          color: 'from-yellow-500 to-orange-600',
          animation: 'pulse-glow',
          glow: 'shadow-yellow-400/50'
        };
      case 'speaking':
        return {
          icon: <Zap className="w-12 h-12 text-blue-400" />,
          color: 'from-blue-500 to-purple-600',
          animation: 'wave-animation',
          glow: 'shadow-blue-400/50'
        };
      default:
        return {
          icon: <Bot className="w-12 h-12 text-white" />,
          color: 'from-gray-500 to-gray-600',
          animation: '',
          glow: 'shadow-gray-400/30'
        };
    }
  };

  const avatarState = getAvatarState();

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Avatar Circle */}
      <motion.div
        className={`relative w-32 h-32 rounded-full bg-gradient-to-br ${avatarState.color} flex items-center justify-center ${avatarState.animation} ${avatarState.glow}`}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, type: "spring" }}
      >
        {avatarState.icon}
        
        {/* Status indicator ring */}
        {status !== 'idle' && (
          <motion.div
            className="absolute inset-0 rounded-full border-4 border-white/20"
            animate={{ 
              scale: [1, 1.1, 1],
              opacity: [0.5, 0.8, 0.5]
            }}
            transition={{ 
              duration: 2, 
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        )}
        
        {/* Inner glow effect */}
        {status !== 'idle' && (
          <motion.div
            className="absolute inset-4 rounded-full bg-white/10"
            animate={{ 
              scale: [0.8, 1, 0.8],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{ 
              duration: 1.5, 
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        )}
      </motion.div>

      {/* Status Text */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h3 className="text-lg font-semibold text-white mb-1">Jarvis</h3>
        <p className={`text-sm capitalize ${
          status === 'listening' ? 'text-green-400' :
          status === 'processing' ? 'text-yellow-400' :
          status === 'speaking' ? 'text-blue-400' :
          'text-gray-400'
        }`}>
          {status === 'idle' ? 'Ready' : status}
        </p>
      </motion.div>

      {/* Connection Status */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex items-center space-x-2"
      >
        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
        <span className="text-xs text-gray-400">Connected</span>
      </motion.div>
    </div>
  );
};

export default JarvisAvatar; 