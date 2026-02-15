import { useState } from "react";
import { Plus, Minus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const faqs = [
  {
    question: "What is Veritas?",
    answer: "Veritas is a multi-agent AI swarm for deepfake detection. It uses five specialised agents — four forensic analysts and one master synthesiser — all powered by Google Gemini, orchestrated via CrewAI. Each agent examines a different signal dimension (biometrics, physics, digital artefacts, audio-visual sync), and their combined evidence produces a final deepfake probability score."
  },
  {
    question: "What technologies power the system?",
    answer: "The backend is built with Python, CrewAI for agent orchestration, and Google Gemini (Flash for workers, Pro for master). The API layer uses FastAPI with Server-Sent Events (SSE) for real-time streaming. The frontend is a React app (Vite + Tailwind CSS + Framer Motion) that renders live agent status and an animated verdict display."
  },
  {
    question: "What kind of files can I upload?",
    answer: "Veritas accepts images (JPG, PNG, WebP) and videos (MP4, MOV). The Sync Specialist agent only provides full analysis (lip-sync, speech cadence, acoustics) when video with audio is uploaded — for still images it will note that audio-visual analysis is not applicable."
  },
  {
    question: "What does the deepfake score mean?",
    answer: "The Chief Justice agent produces a score from 0 to 100, where 0 means very likely authentic and 100 means very likely a deepfake. It also provides a confidence level (HIGH, MEDIUM, LOW), a list of key forensic findings, and a Layman's Brief — a plain-English explanation of the verdict that anyone can understand."
  },
  {
    question: "Is my data stored after analysis?",
    answer: "No. Uploaded files are saved to a temporary location during analysis and are automatically deleted once the scan is complete. No media is retained, logged, or used for training."
  },
  {
    question: "What is mock mode?",
    answer: "When the backend does not detect a GOOGLE_API_KEY in its environment, it automatically runs in mock mode — simulating realistic agent responses with pre-written findings and a sample verdict. This lets you demo the full frontend experience without needing active API credits."
  }
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState(0);

  return (
    <section id="faq" className="py-20 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      <div className="container mx-auto px-4 md:px-6 max-w-4xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-muted text-lg">
            Everything you need to know about Veritas and how it works.
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-white/10 rounded-xl bg-white/5 overflow-hidden transition-all duration-300 hover:border-white/20"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full flex items-center justify-between p-6 text-left focus:outline-none"
              >
                <span className="text-lg font-medium text-white">
                  {faq.question}
                </span>
                <span className="text-accent ml-4 shrink-0">
                  {openIndex === index ? <Minus size={20} /> : <Plus size={20} />}
                </span>
              </button>

              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="px-6 pb-6 text-muted leading-relaxed">
                      {faq.answer}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
