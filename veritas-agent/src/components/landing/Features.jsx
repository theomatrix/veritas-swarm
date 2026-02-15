import { Shield, Eye, Radio, Mic, Brain, Layers } from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    icon: Eye,
    title: "Biometric Sentinel",
    description: "Detects unnatural blink patterns, missing retinal eye-glints, absent pulse signals, and irregular skin micro-texture using AI-powered biometric analysis."
  },
  {
    icon: Shield,
    title: "Physics Inspector",
    description: "Verifies physical plausibility — checks lighting direction, shadow geometry, specular highlight coherence, and reflection accuracy across the scene."
  },
  {
    icon: Radio,
    title: "Signal Analyst",
    description: "Hunts for GAN-induced warping, blending seams, abnormal pixel noise, compression ghosts, and frequency-domain anomalies invisible to the human eye."
  },
  {
    icon: Mic,
    title: "Sync Specialist",
    description: "Evaluates lip-shape alignment with phonemes, speech cadence, room acoustic fingerprints, and detects TTS artefacts in audio tracks."
  },
  {
    icon: Brain,
    title: "Chief Justice (Master Agent)",
    description: "Synthesises all findings into an authoritative deepfake probability score (0-100) and produces a clear Layman's Brief anyone can understand."
  },
  {
    icon: Layers,
    title: "Multi-Agent Swarm Architecture",
    description: "Five AI agents powered by Google Gemini work in concert via CrewAI, with specialist workers feeding evidence to a master synthesiser for maximum accuracy."
  }
];

export function Features() {
  return (
    <section id="features" className="py-20 bg-black/20 relative">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            The Agent Swarm
          </h2>
          <p className="text-muted text-lg">
            Five specialised AI agents analyse your media from every angle — biometrics, physics, digital signals, audio-visual sync — then a master agent delivers the final verdict.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-accent/30 hover:bg-white/10 transition-all duration-300 relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

              <div className="h-12 w-12 rounded-lg bg-accent/10 flex items-center justify-center text-accent mb-4 group-hover:scale-110 transition-transform duration-300">
                <feature.icon size={24} />
              </div>

              <h3 className="text-xl font-semibold text-white mb-2 relative z-10">
                {feature.title}
              </h3>

              <p className="text-muted leading-relaxed relative z-10">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
