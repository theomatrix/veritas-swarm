import { Navbar } from "./Navbar";
import { Footer } from "./Footer";

export function Layout({ children }) {
  return (
    <div className="min-h-screen bg-[#050816] text-white font-sans selection:bg-accent/30 selection:text-accent-glow">
      <Navbar />
      <main className="flex-1 w-full overflow-hidden">
        {children}
      </main>
      <Footer />
    </div>
  );
}
