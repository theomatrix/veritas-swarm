import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Logo } from "./Logo";

export function LoadingScreen({ onComplete }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(timer);
          setTimeout(onComplete, 500); // Wait a bit before unmounting
          return 100;
        }
        return prev + 2; // Adjust speed here
      });
    }, 30);

    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <motion.div
      className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[#050816]"
      exit={{ opacity: 0, transition: { duration: 0.8 } }}
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <Logo size={120} className="animate-pulse" />
      </motion.div>

      <div className="w-64 h-1 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-accent shadow-[0_0_10px_#2F8CFF]"
          initial={{ width: "0%" }}
          animate={{ width: `${progress}%` }}
        />
      </div>

      <p className="mt-4 text-sm text-muted font-mono">Initializing Veritas...</p>
    </motion.div>
  );
}
