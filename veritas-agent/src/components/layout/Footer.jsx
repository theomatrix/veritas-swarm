import { Logo } from "../ui/Logo";
import { Link } from "react-router-dom";

export function Footer() {
  return (
    <footer className="bg-black/40 border-t border-white/10 py-12 md:py-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-10">
          <div className="md:col-span-1">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <Logo size={32} />
              <div className="flex flex-col">
                <span className="text-xl font-bold tracking-tight text-white leading-tight">
                  Veritas
                </span>
                <span className="text-[10px] text-muted font-medium tracking-widest uppercase leading-tight">
                  Agent Swarm for Deepfake Detection
                </span>
              </div>
            </Link>
            <p className="text-muted text-sm leading-relaxed">
              Multi-agent deepfake detection powered by Google Gemini and CrewAI. Upload. Analyse. Know the truth.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-4">Product</h3>
            <ul className="space-y-2 text-sm text-muted">
              <li><a href="#features" className="hover:text-accent transition-colors">The Swarm</a></li>
              <li><a href="#process" className="hover:text-accent transition-colors">How It Works</a></li>
              <li><Link to="/scan" className="hover:text-accent transition-colors">Launch Scanner</Link></li>
              <li><a href="#faq" className="hover:text-accent transition-colors">FAQ</a></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-4">Tech Stack</h3>
            <ul className="space-y-2 text-sm text-muted">
              <li><span className="text-white/60">Backend:</span> FastAPI + CrewAI</li>
              <li><span className="text-white/60">LLM:</span> Google Gemini</li>
              <li><span className="text-white/60">Frontend:</span> React + Vite</li>
              <li><span className="text-white/60">Streaming:</span> SSE</li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-4">Project</h3>
            <ul className="space-y-2 text-sm text-muted">
              <li><a href="https://github.com" target="_blank" rel="noopener noreferrer" className="hover:text-accent transition-colors">GitHub Repository</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">License</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted">
          <p>© {new Date().getFullYear()} Veritas. All rights reserved.</p>
          <div className="flex items-center gap-1">
            <span>Made with</span>
            <span className="text-red-500">♥</span>
            <span> by team vigilante</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
