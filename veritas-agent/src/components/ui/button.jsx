import React from "react";
import { cn } from "../../lib/utils";
import { Loader2 } from "lucide-react";

export const Button = React.forwardRef(
  ({ className, variant = "primary", size = "md", isLoading, children, ...props }, ref) => {
    const variants = {
      primary: "bg-accent hover:bg-accent-glow text-white shadow-lg shadow-accent/20 border border-transparent",
      secondary: "bg-white/5 border border-white/10 hover:border-accent/50 text-white hover:bg-white/10",
      outline: "bg-transparent border border-accent text-accent hover:bg-accent/10",
      ghost: "bg-transparent hover:bg-white/5 text-muted hover:text-white",
    };

    const sizes = {
      sm: "h-8 px-3 text-xs",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    };

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-full font-medium transition-all duration-300 disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
          variants[variant],
          sizes[size],
          className
        )}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
