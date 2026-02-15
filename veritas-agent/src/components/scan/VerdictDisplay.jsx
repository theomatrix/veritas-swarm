import { motion } from "framer-motion";
import { cn } from "../../lib/utils";
import { AlertTriangle, CheckCircle2, HelpCircle, RotateCcw, FlaskConical } from "lucide-react";
import { Button } from "../ui/button";

function ScoreGauge({ score }) {
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    // Color based on score
    const getColor = (s) => {
        if (s <= 30) return { stroke: "#22c55e", glow: "rgba(34, 197, 94, 0.4)", label: "Likely Authentic" };
        if (s <= 60) return { stroke: "#eab308", glow: "rgba(234, 179, 8, 0.4)", label: "Suspicious" };
        return { stroke: "#ef4444", glow: "rgba(239, 68, 68, 0.4)", label: "Likely Deepfake" };
    };

    const color = getColor(score);

    return (
        <div className="relative flex flex-col items-center">
            <svg width="160" height="160" viewBox="0 0 100 100" className="transform -rotate-90">
                {/* Background circle */}
                <circle
                    cx="50" cy="50" r={radius}
                    fill="none"
                    stroke="rgba(255,255,255,0.08)"
                    strokeWidth="8"
                />
                {/* Score arc */}
                <motion.circle
                    cx="50" cy="50" r={radius}
                    fill="none"
                    stroke={color.stroke}
                    strokeWidth="8"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset: offset }}
                    transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
                    style={{ filter: `drop-shadow(0 0 8px ${color.glow})` }}
                />
            </svg>

            {/* Score number overlay */}
            <motion.div
                className="absolute inset-0 flex flex-col items-center justify-center"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.8, duration: 0.5 }}
            >
                <span className="text-4xl font-bold text-white" style={{ textShadow: `0 0 20px ${color.glow}` }}>
                    {score}
                </span>
                <span className="text-xs text-muted font-mono mt-0.5">/ 100</span>
            </motion.div>

            {/* Label */}
            <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 }}
                className="mt-3 text-sm font-semibold"
                style={{ color: color.stroke }}
            >
                {color.label}
            </motion.p>
        </div>
    );
}

function ConfidenceBadge({ level }) {
    const config = {
        HIGH: { color: "bg-green-500/20 text-green-400 border-green-500/30", icon: CheckCircle2 },
        MEDIUM: { color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30", icon: HelpCircle },
        LOW: { color: "bg-red-500/20 text-red-400 border-red-500/30", icon: AlertTriangle },
    };
    const c = config[level] || config.MEDIUM;
    const Icon = c.icon;

    return (
        <div className={cn("inline-flex items-center gap-2 px-3 py-1 rounded-full border text-xs font-semibold", c.color)}>
            <Icon size={14} />
            {level} Confidence
        </div>
    );
}

export function VerdictDisplay({ verdict, onReset, isMock }) {
    if (!verdict) return null;

    const { score, confidence, findings, laymans_brief } = verdict;

    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="w-full max-w-3xl mx-auto space-y-6"
        >
            {/* Score + Confidence Header */}
            <div className="flex flex-col items-center gap-4 py-6">
                <motion.h2
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-2xl font-bold text-white flex items-center gap-2"
                >
                    ⚖️ Final Verdict
                </motion.h2>

                {isMock && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 text-xs font-semibold"
                    >
                        <FlaskConical size={12} />
                        SIMULATED DATA
                    </motion.div>
                )}

                <ScoreGauge score={score} />
                <ConfidenceBadge level={confidence} />
            </div>

            {/* Key Findings */}
            {findings && findings.length > 0 && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.0 }}
                    className="rounded-2xl p-6 bg-white/5 border border-white/10 backdrop-blur-sm"
                >
                    <h3 className="text-sm font-semibold text-accent mb-4 uppercase tracking-wider">
                        Key Findings
                    </h3>
                    <ul className="space-y-3">
                        {findings.map((finding, i) => (
                            <motion.li
                                key={i}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 1.2 + i * 0.1 }}
                                className="flex items-start gap-3 text-sm text-muted"
                            >
                                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-1.5 flex-shrink-0" />
                                <span>{finding}</span>
                            </motion.li>
                        ))}
                    </ul>
                </motion.div>
            )}

            {/* Layman's Brief */}
            {laymans_brief && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.5 }}
                    className="rounded-2xl p-6 border border-accent/20 bg-gradient-to-br from-accent/5 to-purple-500/5 backdrop-blur-sm"
                >
                    <h3 className="text-sm font-semibold text-accent-glow mb-3 uppercase tracking-wider flex items-center gap-2">
                        💡 Layman's Brief
                    </h3>
                    <p className="text-base text-white/80 leading-relaxed">
                        {laymans_brief}
                    </p>
                </motion.div>
            )}

            {/* Reset Button */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 2.0 }}
                className="flex justify-center pt-4"
            >
                <Button
                    variant="secondary"
                    size="lg"
                    onClick={onReset}
                    className="gap-2"
                >
                    <RotateCcw size={16} />
                    Scan Another File
                </Button>
            </motion.div>
        </motion.div>
    );
}
