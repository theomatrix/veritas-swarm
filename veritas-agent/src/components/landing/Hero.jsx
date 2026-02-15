import { Button } from "../ui/button";
import { ArrowRight, Shield, CheckCircle2 } from "lucide-react";
import { Logo } from "../ui/Logo";
import { Link } from "react-router-dom";

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1200px] h-[600px] bg-glow-radial opacity-40 pointer-events-none" />

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">

          {/* Left Column: Copy */}
          <div className="text-center lg:text-left space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-accent animate-in fade-in slide-in-from-bottom-4 duration-1000">
              <Shield size={12} />
              <span>Multi-Agent Deepfake Detection</span>
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-tight text-white animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-100">
              Truth in the <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-accent-glow text-glow">
                Age of AI
              </span>
            </h1>

            <p className="text-lg text-muted max-w-xl mx-auto lg:mx-0 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-200">
              Five specialised AI agents powered by Google Gemini analyse your media from every angle — biometrics, physics, digital signals, and audio-visual sync — to deliver an authoritative deepfake verdict.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-300">
              <Link to="/scan">
                <Button size="lg" className="w-full sm:w-auto group bg-accent hover:bg-accent/90 text-white shadow-[0_0_20px_rgba(47,140,255,0.3)]">
                  Start Detection
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Button variant="secondary" size="lg" className="w-full sm:w-auto border-white/10 hover:bg-white/5 text-white">
                View Methodology
              </Button>
            </div>

            <div className="pt-4 flex items-center justify-center lg:justify-start gap-6 text-sm text-muted animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-400">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500" />
                <span>Real-time Analysis</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-accent" />
                <span>API Ready</span>
              </div>
            </div>
          </div>

          {/* Right Column: Visual */}
          <div className="relative flex items-center justify-center animate-in fade-in zoom-in duration-1000 delay-500">
            {/* Glow backing */}
            <div className="absolute inset-0 bg-accent/20 blur-[100px] rounded-full" />

            {/* Main Logo Visualization */}
            <div className="relative z-10 p-12 border border-white/10 bg-white/5 backdrop-blur-xl rounded-3xl shadow-2xl ring-1 ring-white/10">
              <Logo size={300} animated={true} className="text-accent drop-shadow-[0_0_30px_rgba(47,140,255,0.8)]" />

              {/* Floating Elements */}
              <div className="absolute -top-6 -right-6 p-4 bg-[#0A0F2C] border border-accent/30 rounded-xl shadow-lg animate-bounce duration-[3000ms]">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-xs font-mono text-accent-glow">System Active</span>
                </div>
              </div>

              <div className="absolute -bottom-8 -left-8 p-4 bg-[#0A0F2C] border border-red-500/30 rounded-xl shadow-lg animate-bounce duration-[4000ms]">
                <div className="flex items-center gap-3">
                  <Shield className="w-4 h-4 text-red-400" />
                  <span className="text-xs font-mono text-white">Threats Blocked</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
