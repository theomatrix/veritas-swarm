import { motion, AnimatePresence } from "framer-motion";
import { Shield, Eye, Radio, Mic, Brain, Check, Loader2 } from "lucide-react";
import { cn } from "../../lib/utils";

const AGENT_CONFIG = {
    "Biometric Sentinel": {
        icon: Eye,
        color: "from-emerald-500 to-teal-500",
        ringColor: "ring-emerald-500/30",
        glowColor: "rgba(16, 185, 129, 0.3)",
        description: "Analyzing blinks, pulse & eye glints",
    },
    "Physics Inspector": {
        icon: Shield,
        color: "from-blue-500 to-cyan-500",
        ringColor: "ring-blue-500/30",
        glowColor: "rgba(59, 130, 246, 0.3)",
        description: "Checking lighting, shadows & reflections",
    },
    "Signal Analyst": {
        icon: Radio,
        color: "from-purple-500 to-pink-500",
        ringColor: "ring-purple-500/30",
        glowColor: "rgba(168, 85, 247, 0.3)",
        description: "Hunting warping, noise & seams",
    },
    "Sync Specialist": {
        icon: Mic,
        color: "from-orange-500 to-amber-500",
        ringColor: "ring-orange-500/30",
        glowColor: "rgba(249, 115, 22, 0.3)",
        description: "Evaluating lip-sync & acoustics",
    },
};

export function AgentStatusPanel({ agents, masterStatus, onAgentClick }) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="w-full max-w-4xl mx-auto space-y-6"
        >
            {/* Agent Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {Object.entries(AGENT_CONFIG).map(([name, config], index) => {
                    const agentData = agents[name];
                    const status = agentData?.status || "waiting";
                    const Icon = config.icon;

                    return (
                        <motion.div
                            key={name}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.15, duration: 0.5 }}
                            onClick={() => agentData?.findings && onAgentClick?.(name)}
                            className={cn(
                                "relative rounded-2xl p-5 border transition-all duration-500 overflow-hidden",
                                "bg-white/5 backdrop-blur-sm",
                                status === "analyzing" && "border-accent/40",
                                status === "complete" && "border-green-500/30 cursor-pointer hover:bg-white/10",
                                status === "waiting" && "border-white/10"
                            )}
                        >
                            {/* Background glow when analyzing */}
                            {status === "analyzing" && (
                                <div
                                    className="absolute inset-0 opacity-20 blur-3xl"
                                    style={{ background: `radial-gradient(circle, ${config.glowColor}, transparent)` }}
                                />
                            )}

                            <div className="relative z-10 flex items-start gap-4">
                                {/* Icon with status indicator */}
                                <div className="relative">
                                    <div className={cn(
                                        "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-500",
                                        status === "analyzing" && `bg-gradient-to-br ${config.color} shadow-lg`,
                                        status === "complete" && "bg-green-500/20",
                                        status === "waiting" && "bg-white/5"
                                    )}>
                                        {status === "complete" ? (
                                            <Check size={22} className="text-green-400" />
                                        ) : status === "analyzing" ? (
                                            <Icon size={22} className="text-white" />
                                        ) : (
                                            <Icon size={22} className="text-muted/50" />
                                        )}
                                    </div>

                                    {/* Pulse ring when analyzing */}
                                    {status === "analyzing" && (
                                        <div className={cn(
                                            "absolute inset-0 rounded-xl ring-2 animate-pulse-ring",
                                            config.ringColor
                                        )} />
                                    )}
                                </div>

                                {/* Text */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-1">
                                        <h3 className={cn(
                                            "text-sm font-semibold transition-colors",
                                            status === "waiting" ? "text-muted/50" : "text-white"
                                        )}>
                                            {name}
                                        </h3>
                                        {status === "analyzing" && (
                                            <Loader2 size={14} className="text-accent animate-spin" />
                                        )}
                                    </div>

                                    <p className={cn(
                                        "text-xs transition-colors",
                                        status === "waiting" ? "text-muted/30" : "text-muted"
                                    )}>
                                        {status === "complete"
                                            ? "Analysis complete — click to view"
                                            : status === "analyzing"
                                                ? config.description
                                                : "Waiting to start..."}
                                    </p>

                                    {/* Findings preview */}
                                    <AnimatePresence>
                                        {status === "complete" && agentData?.findings && (
                                            <motion.div
                                                initial={{ height: 0, opacity: 0 }}
                                                animate={{ height: "auto", opacity: 1 }}
                                                transition={{ duration: 0.3 }}
                                                className="mt-2 overflow-hidden"
                                            >
                                                <p className="text-xs text-muted/70 line-clamp-2 font-mono">
                                                    {agentData.findings.substring(0, 120)}...
                                                </p>
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </div>
                            </div>

                            {/* Progress bar */}
                            {status === "analyzing" && (
                                <div className="mt-3 h-0.5 rounded-full bg-white/10 overflow-hidden">
                                    <motion.div
                                        className={`h-full bg-gradient-to-r ${config.color}`}
                                        initial={{ width: "0%" }}
                                        animate={{ width: "90%" }}
                                        transition={{ duration: 8, ease: "linear" }}
                                    />
                                </div>
                            )}
                        </motion.div>
                    );
                })}
            </div>

            {/* Master Agent / Chief Justice */}
            <AnimatePresence>
                {masterStatus && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        transition={{ duration: 0.5 }}
                        className="relative rounded-2xl p-6 border border-accent/30 bg-gradient-to-br from-accent/10 via-white/5 to-purple-500/10 backdrop-blur-sm overflow-hidden"
                    >
                        {/* Animated background */}
                        <div className="absolute inset-0 bg-gradient-to-r from-accent/5 via-transparent to-purple-500/5 opacity-50" />

                        <div className="relative z-10 flex items-center gap-4">
                            <div className="relative">
                                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent to-purple-500 flex items-center justify-center shadow-lg shadow-accent/30 animate-brain-pulse">
                                    <Brain size={28} className="text-white" />
                                </div>
                            </div>

                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-1">
                                    <h3 className="text-base font-bold text-white">Chief Justice</h3>
                                    <span className="text-xs font-mono text-accent bg-accent/10 px-2 py-0.5 rounded-full">
                                        MASTER AGENT
                                    </span>
                                </div>
                                <p className="text-sm text-muted flex items-center gap-2">
                                    <Loader2 size={14} className="animate-spin text-accent" />
                                    Synthesizing findings from all agents into final verdict...
                                </p>
                            </div>
                        </div>

                        {/* Progress */}
                        <div className="mt-4 h-1 rounded-full bg-white/10 overflow-hidden">
                            <motion.div
                                className="h-full bg-gradient-to-r from-accent to-purple-500"
                                initial={{ width: "0%" }}
                                animate={{ width: "85%" }}
                                transition={{ duration: 6, ease: "linear" }}
                            />
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
