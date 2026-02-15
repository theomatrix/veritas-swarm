import { useState, useRef, useCallback } from "react";
import { Upload, X, FileImage, FileVideo } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../lib/utils";

export function UploadZone({ onFileSelect, disabled }) {
    const [isDragging, setIsDragging] = useState(false);
    const [preview, setPreview] = useState(null);
    const [file, setFile] = useState(null);
    const inputRef = useRef(null);

    const handleFile = useCallback((f) => {
        if (!f) return;
        setFile(f);

        // Generate preview for images
        if (f.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => setPreview({ url: e.target.result, type: "image" });
            reader.readAsDataURL(f);
        } else if (f.type.startsWith("video/")) {
            setPreview({ url: URL.createObjectURL(f), type: "video" });
        }

        onFileSelect?.(f);
    }, [onFileSelect]);

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const f = e.dataTransfer.files?.[0];
        handleFile(f);
    };

    const handleRemove = () => {
        setPreview(null);
        setFile(null);
        onFileSelect?.(null);
        if (inputRef.current) inputRef.current.value = "";
    };

    const isImage = file?.type?.startsWith("image/");
    const isVideo = file?.type?.startsWith("video/");

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="w-full max-w-2xl mx-auto"
        >
            <AnimatePresence mode="wait">
                {!preview ? (
                    <motion.div
                        key="dropzone"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                        onDragLeave={() => setIsDragging(false)}
                        onDrop={handleDrop}
                        onClick={() => !disabled && inputRef.current?.click()}
                        className={cn(
                            "relative cursor-pointer rounded-2xl p-12 text-center transition-all duration-300",
                            "border-2 border-dashed",
                            isDragging
                                ? "border-accent bg-accent/10 scale-[1.02]"
                                : "border-white/20 hover:border-accent/50 hover:bg-white/5",
                            disabled && "pointer-events-none opacity-50"
                        )}
                    >
                        {/* Animated gradient border on hover */}
                        <div className={cn(
                            "absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-500",
                            isDragging && "opacity-100"
                        )}>
                            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-accent/20 via-accent-glow/20 to-accent/20 animate-border-dance" />
                        </div>

                        <div className="relative z-10 flex flex-col items-center gap-4">
                            <div className={cn(
                                "w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-300",
                                isDragging ? "bg-accent/20 text-accent scale-110" : "bg-white/5 text-muted"
                            )}>
                                <Upload size={28} />
                            </div>

                            <div>
                                <p className="text-lg font-semibold text-white mb-1">
                                    Drop your file here or click to browse
                                </p>
                                <p className="text-sm text-muted">
                                    Supports images (JPG, PNG, WebP) and videos (MP4, MOV)
                                </p>
                            </div>

                            <div className="flex items-center gap-3 text-xs text-muted/60">
                                <span className="flex items-center gap-1"><FileImage size={14} /> Images</span>
                                <span className="w-1 h-1 rounded-full bg-white/20" />
                                <span className="flex items-center gap-1"><FileVideo size={14} /> Videos</span>
                            </div>
                        </div>

                        <input
                            ref={inputRef}
                            type="file"
                            accept="image/*,video/*"
                            onChange={(e) => handleFile(e.target.files?.[0])}
                            className="hidden"
                        />
                    </motion.div>
                ) : (
                    <motion.div
                        key="preview"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="relative rounded-2xl overflow-hidden border border-white/10 bg-white/5"
                    >
                        {/* Preview */}
                        <div className="relative aspect-video flex items-center justify-center bg-black/40">
                            {isImage && (
                                <img
                                    src={preview.url}
                                    alt="Preview"
                                    className="max-h-full max-w-full object-contain"
                                />
                            )}
                            {isVideo && (
                                <video
                                    src={preview.url}
                                    className="max-h-full max-w-full object-contain"
                                    controls
                                    muted
                                />
                            )}

                            {/* Remove button */}
                            {!disabled && (
                                <button
                                    onClick={handleRemove}
                                    className="absolute top-3 right-3 p-2 rounded-full bg-black/60 hover:bg-red-500/80 text-white transition-all duration-200 backdrop-blur-sm"
                                >
                                    <X size={16} />
                                </button>
                            )}
                        </div>

                        {/* File info */}
                        <div className="p-4 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                {isImage ? <FileImage size={18} className="text-accent" /> : <FileVideo size={18} className="text-accent" />}
                                <div>
                                    <p className="text-sm font-medium text-white truncate max-w-[300px]">
                                        {file?.name}
                                    </p>
                                    <p className="text-xs text-muted">
                                        {(file?.size / 1024 / 1024).toFixed(2)} MB
                                    </p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                <span className="text-xs text-green-400 font-mono">Ready</span>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
