import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/LandingPage";
import { ScanPage } from "./pages/ScanPage";
import { LoadingScreen } from "./components/ui/LoadingScreen";
import { AnimatePresence } from "framer-motion";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <BrowserRouter>
      <AnimatePresence>
        {isLoading && <LoadingScreen onComplete={() => setIsLoading(false)} />}
      </AnimatePresence>
      {!isLoading && (
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/scan" element={<ScanPage />} />
        </Routes>
      )}
    </BrowserRouter>
  );
}

export default App;
