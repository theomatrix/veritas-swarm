import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../lib/utils";

const steps = [
  {
    id: "upload",
    label: "1. Upload",
    title: "Upload Your Media",
    content: "Drag and drop any image or video file into the Veritas scanner. The file is streamed to the backend and saved in a temporary secure location for analysis — it is never stored permanently."
  },
  {
    id: "workers",
    label: "2. Swarm Analysis",
    title: "Four Specialist Agents Investigate",
    content: "The Biometric Sentinel, Physics Inspector, Signal Analyst, and Sync Specialist — each powered by Google Gemini Flash — analyse the media sequentially. Each agent examines a different forensic dimension: biological signals, lighting physics, digital artefacts, and audio-visual sync."
  },
  {
    id: "master",
    label: "3. Synthesis",
    title: "Chief Justice Delivers the Verdict",
    content: "All four reports are fed to the Chief Justice, powered by Google Gemini Pro. It weighs the evidence, resolves conflicting signals, and produces a deepfake probability score (0–100), a confidence rating, key findings, and a plain-English Layman's Brief."
  },
  {
    id: "streaming",
    label: "4. Real-time Results",
    title: "Live Agent Status via SSE",
    content: "You watch the entire analysis unfold in real time. The FastAPI backend streams Server-Sent Events (SSE) as each agent starts and finishes — so you see thinking indicators, progress bars, and the final verdict with animated gauges, all without page reloads."
  }
];

export function UseCases() {
  const [activeTab, setActiveTab] = useState(steps[0].id);

  return (
    <section id="process" className="py-20 bg-black/40">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            How Veritas Works
          </h2>
          <p className="text-muted text-lg">
            From file upload to final verdict — here's how the multi-agent pipeline works end to end.
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-8 md:gap-12 max-w-5xl mx-auto">
          {/* Tabs */}
          <div className="flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-4 md:pb-0 md:w-1/3 shrink-0">
            {steps.map((step) => (
              <button
                key={step.id}
                onClick={() => setActiveTab(step.id)}
                className={cn(
                  "px-6 py-4 rounded-xl text-left transition-all duration-300 border whitespace-nowrap md:whitespace-normal",
                  activeTab === step.id
                    ? "bg-accent/10 border-accent text-white shadow-lg shadow-accent/5"
                    : "bg-transparent border-transparent text-muted hover:bg-white/5 hover:text-white"
                )}
              >
                <span className="font-semibold block">{step.label}</span>
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="md:w-2/3 min-h-[200px]">
            <AnimatePresence mode="wait">
              {steps.map((step) => (
                activeTab === step.id && (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                    className="bg-white/5 border border-white/10 rounded-2xl p-8 h-full flex flex-col justify-center"
                  >
                    <h3 className="text-2xl font-bold text-white mb-4">
                      {step.title}
                    </h3>
                    <p className="text-muted text-lg leading-relaxed">
                      {step.content}
                    </p>
                    <div className="mt-6 pt-6 border-t border-white/10 flex items-center gap-4">
                      <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                      <span className="text-sm font-medium text-accent">
                        {step.id === "upload" ? "Supports JPG, PNG, WebP, MP4, MOV" :
                          step.id === "workers" ? "Powered by Gemini 2.0 Flash" :
                            step.id === "master" ? "Powered by Gemini 2.0 Pro" :
                              "FastAPI + Server-Sent Events"}
                      </span>
                    </div>
                  </motion.div>
                )
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  );
}
