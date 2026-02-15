import { Layout } from "../components/layout/Layout";
import { Hero } from "../components/landing/Hero";
import { Features } from "../components/landing/Features";
import { UseCases } from "../components/landing/UseCases";
import { FAQ } from "../components/landing/FAQ";
import { Button } from "../components/ui/button";
import { Link } from "react-router-dom";
import { Zap } from "lucide-react";

export function LandingPage() {
  return (
    <Layout>
      <Hero />
      <Features />
      <UseCases />

      {/* CTA Strip */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-accent/10" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#050816] via-transparent to-[#050816]" />

        <div className="container mx-auto px-4 text-center relative z-10">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Ready to detect deepfakes?
          </h2>
          <p className="text-lg text-muted mb-8 max-w-2xl mx-auto">
            Upload an image or video and let the Veritas agent swarm analyse it in real time. Five AI agents. One definitive verdict.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/scan">
              <Button size="lg" className="px-8 text-base gap-2 bg-accent hover:bg-accent/90 text-white shadow-[0_0_20px_rgba(47,140,255,0.3)]">
                <Zap size={18} />
                Launch Scanner
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <FAQ />
    </Layout>
  );
}
