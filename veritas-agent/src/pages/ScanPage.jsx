import { useState, useCallback, useEffect } from "react";
import { Layout } from "../components/layout/Layout";
import { UploadZone } from "../components/scan/UploadZone";
import { AgentStatusPanel } from "../components/scan/AgentStatusPanel";
import { VerdictDisplay } from "../components/scan/VerdictDisplay";
import { Button } from "../components/ui/button";
import { motion, AnimatePresence } from "framer-motion";
import { Zap, ArrowLeft, FlaskConical } from "lucide-react";
import { Link } from "react-router-dom";

// Phases: upload → analyzing → verdict
const PHASE = { UPLOAD: "upload", ANALYZING: "analyzing", VERDICT: "verdict" };

export function ScanPage() {
    const [phase, setPhase] = useState(PHASE.UPLOAD);
    const [file, setFile] = useState(null);
    const [agents, setAgents] = useState({});
    const [masterStatus, setMasterStatus] = useState(false);
    const [verdict, setVerdict] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [selectedAgent, setSelectedAgent] = useState(null);
    const [isMock, setIsMock] = useState(false);

    // Check if backend is running in mock mode
    useEffect(() => {
        fetch("/api/health")
            .then((res) => res.json())
            .then((data) => setIsMock(data.mock === true))
            .catch(() => setIsMock(false));
    }, []);

    const handleAnalyze = useCallback(async () => {
        if (!file) return;
        setIsUploading(true);
        setPhase(PHASE.ANALYZING);
        setAgents({});
        setMasterStatus(false);
        setVerdict(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData,
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Process complete SSE lines
                const lines = buffer.split("\n");
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (!line.startsWith("data: ")) continue;
                    const jsonStr = line.slice(6).trim();
                    if (!jsonStr) continue;

                    try {
                        const event = JSON.parse(jsonStr);

                        switch (event.type) {
                            case "agent_start":
                                setAgents((prev) => ({
                                    ...prev,
                                    [event.agent]: { status: "analyzing", findings: null },
                                }));
                                break;

                            case "agent_complete":
                                setAgents((prev) => ({
                                    ...prev,
                                    [event.agent]: { status: "complete", findings: event.findings },
                                }));
                                break;

                            case "master_start":
                                setMasterStatus(true);
                                break;

                            case "verdict":
                                setMasterStatus(false);
                                setVerdict(event);
                                setPhase(PHASE.VERDICT);
                                break;

                            case "error":
                                console.error("Agent error:", event.message);
                                break;

                            case "done":
                                break;
                        }
                    } catch {
                        // Skip malformed JSON
                    }
                }
            }
        } catch (err) {
            console.error("Analysis failed:", err);
        } finally {
            setIsUploading(false);
        }
    }, [file]);

    const handleReset = () => {
        setPhase(PHASE.UPLOAD);
        setFile(null);
        setAgents({});
        setMasterStatus(false);
        setVerdict(null);
        setSelectedAgent(null);
    };

    return (
        <Layout>
            <section className="relative pt-28 pb-20 min-h-screen">
                {/* Background glow */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-[500px] bg-glow-radial opacity-30 pointer-events-none" />

                <div className="container mx-auto px-4 relative z-10">
                    {/* Back link */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="mb-8"
                    >
                        <Link
                            to="/"
                            className="inline-flex items-center gap-2 text-sm text-muted hover:text-white transition-colors"
                        >
                            <ArrowLeft size={16} />
                            Back to Home
                        </Link>
                    </motion.div>

                    {/* Mock Mode Banner */}
                    {isMock && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mb-6 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 text-sm font-medium max-w-xl mx-auto"
                        >
                            <FlaskConical size={16} />
                            <span>Demo Mode — Results below are simulated mock data for testing purposes</span>
                        </motion.div>
                    )}

                    {/* Header */}
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center mb-10"
                    >
                        <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
                            Deepfake{" "}
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-accent-glow text-glow">
                                Scanner
                            </span>
                        </h1>
                        <p className="text-muted max-w-lg mx-auto">
                            Upload an image or video and let our AI agent swarm analyze it for signs
                            of synthetic manipulation.
                        </p>
                    </motion.div>

                    {/* Phase Content */}
                    <AnimatePresence mode="wait">
                        {phase === PHASE.UPLOAD && (
                            <motion.div
                                key="upload"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0, y: -20 }}
                                className="space-y-6"
                            >
                                <UploadZone onFileSelect={setFile} disabled={isUploading} />

                                {file && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="flex justify-center"
                                    >
                                        <Button
                                            size="lg"
                                            className="gap-2 bg-accent hover:bg-accent/90 text-white shadow-[0_0_25px_rgba(47,140,255,0.3)] px-10"
                                            onClick={handleAnalyze}
                                            isLoading={isUploading}
                                        >
                                            <Zap size={18} />
                                            Deploy Agent Swarm
                                        </Button>
                                    </motion.div>
                                )}
                            </motion.div>
                        )}

                        {phase === PHASE.ANALYZING && (
                            <motion.div
                                key="analyzing"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                            >
                                <AgentStatusPanel
                                    agents={agents}
                                    masterStatus={masterStatus}
                                    onAgentClick={setSelectedAgent}
                                />
                            </motion.div>
                        )}

                        {phase === PHASE.VERDICT && (
                            <motion.div
                                key="verdict"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                            >
                                <VerdictDisplay verdict={verdict} onReset={handleReset} isMock={isMock} />
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Agent Detail Modal */}
                    <AnimatePresence>
                        {selectedAgent && agents[selectedAgent]?.findings && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
                                onClick={() => setSelectedAgent(null)}
                            >
                                <motion.div
                                    initial={{ scale: 0.9, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    exit={{ scale: 0.9, opacity: 0 }}
                                    className="bg-[#0A0F2C] border border-white/10 rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto"
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="text-lg font-bold text-white">{selectedAgent}</h3>
                                        <button
                                            onClick={() => setSelectedAgent(null)}
                                            className="text-muted hover:text-white transition-colors"
                                        >
                                            ✕
                                        </button>
                                    </div>
                                    <pre className="text-sm text-muted whitespace-pre-wrap font-mono leading-relaxed">
                                        {agents[selectedAgent].findings}
                                    </pre>
                                </motion.div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </section>
        </Layout>
    );
}
