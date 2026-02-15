import { useState, useEffect } from "react";
import { Button } from "../ui/button";
import { Menu, X } from "lucide-react";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { Logo } from "../ui/Logo";
import { Link, useLocation } from "react-router-dom";

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const isLanding = location.pathname === "/";

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Features", href: "#features" },
    { name: "How it Works", href: "#process" },
    { name: "Use Cases", href: "#use-cases" },
    { name: "FAQ", href: "#faq" },
  ];

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        isScrolled ? "bg-[#050816]/80 backdrop-blur-md border-b border-white/10 py-3" : "bg-transparent py-5"
      )}
    >
      <div className="container mx-auto px-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
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

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          {isLanding && navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="text-sm font-medium text-muted hover:text-white transition-colors"
            >
              {link.name}
            </a>
          ))}
          <Link
            to="/scan"
            className={cn(
              "text-sm font-medium transition-colors",
              location.pathname === "/scan" ? "text-accent" : "text-muted hover:text-white"
            )}
          >
            Scan
          </Link>
        </nav>

        <div className="hidden md:flex items-center gap-4">
          <a href="#contact" className="text-sm font-medium text-white hover:text-accent transition-colors">
            Contact
          </a>
          <Link to="/scan">
            <Button variant="primary" size="sm" className="bg-white text-black hover:bg-white/90">Get Started</Button>
          </Link>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-white"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-[#050816] border-b border-white/10 overflow-hidden"
          >
            <div className="container px-4 py-6 flex flex-col gap-4">
              {isLanding && navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="text-base font-medium text-muted hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.name}
                </a>
              ))}
              <Link
                to="/scan"
                className="text-base font-medium text-accent"
                onClick={() => setMobileMenuOpen(false)}
              >
                Scan
              </Link>
              <div className="h-px bg-white/10 my-2" />
              <Link to="/scan" onClick={() => setMobileMenuOpen(false)}>
                <Button className="w-full bg-accent text-white">Get Started</Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
