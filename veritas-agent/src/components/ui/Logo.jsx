import React from "react";
import { cn } from "../../lib/utils";

export function Logo({ className, size = 32, animated = false }) {
  return (
    <div
      className={cn("relative flex items-center justify-center", className)}
      style={{ width: size, height: size }}
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="text-accent drop-shadow-[0_0_10px_rgba(47,140,255,0.6)]"
      >
        {/* Outer Shield/V Shape */}
        <path
          d="M50 95L15 30H85L50 95Z"
          stroke="currentColor"
          strokeWidth="4"
          fill="none"
          className="animate-[pulse_3s_ease-in-out_infinite]"
        />
        {/* Inner Eye/Lens */}
        <circle cx="50" cy="45" r="12" stroke="currentColor" strokeWidth="4" className="text-white" />
        <circle cx="50" cy="45" r="6" fill="currentColor" className="text-accent-glow" />

        {/* Scan Lines */}
        <path d="M25 30L50 80L75 30" stroke="currentColor" strokeWidth="1" strokeOpacity="0.5" />

        {/* Top Bar */}
        <path d="M10 30H90" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />

        {/* Animated Scan Line — horizontal sweep */}
        {animated && (
          <g className="animate-scan-line">
            <line
              x1="20" y1="50" x2="80" y2="50"
              stroke="url(#scanGradient)"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <rect
              x="20" y="48" width="60" height="4"
              fill="url(#scanGlow)"
              opacity="0.4"
              rx="2"
            />
          </g>
        )}

        {/* Floating particles around the eye */}
        {animated && (
          <>
            <circle cx="35" cy="38" r="1.5" fill="#5AF0FF" opacity="0.6" className="animate-particle" />
            <circle cx="65" cy="38" r="1" fill="#2F8CFF" opacity="0.5" className="animate-particle" style={{ animationDelay: "0.5s" }} />
            <circle cx="42" cy="55" r="1.2" fill="#5AF0FF" opacity="0.4" className="animate-particle" style={{ animationDelay: "1s" }} />
            <circle cx="58" cy="55" r="1" fill="#2F8CFF" opacity="0.5" className="animate-particle" style={{ animationDelay: "1.5s" }} />
          </>
        )}

        {/* Gradient defs */}
        <defs>
          <linearGradient id="scanGradient" x1="20" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#2F8CFF" stopOpacity="0" />
            <stop offset="50%" stopColor="#5AF0FF" stopOpacity="1" />
            <stop offset="100%" stopColor="#2F8CFF" stopOpacity="0" />
          </linearGradient>
          <linearGradient id="scanGlow" x1="20" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#5AF0FF" stopOpacity="0" />
            <stop offset="50%" stopColor="#5AF0FF" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#5AF0FF" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}
