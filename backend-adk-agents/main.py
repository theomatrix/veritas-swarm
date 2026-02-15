"""
Veritas Swarm — CLI Entry Point
Run:  python main.py <path-to-image-or-video>
"""

import sys
from crew import VeritasCrew

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   ██╗   ██╗███████╗██████╗ ██╗████████╗ █████╗ ███████╗  ║
║   ██║   ██║██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗██╔════╝  ║
║   ██║   ██║█████╗  ██████╔╝██║   ██║   ███████║███████╗  ║
║   ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║   ██╔══██║╚════██║  ║
║    ╚████╔╝ ███████╗██║  ██║██║   ██║   ██║  ██║███████║  ║
║     ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝  ║
║                                                      ║
║          S W A R M   D E E P F A K E                 ║
║              D E T E C T O R                         ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""

DIVIDER = "═" * 56


def main():
    print(BANNER)

    # ── Parse CLI argument ──────────────────────────────────────────────
    if len(sys.argv) < 2:
        print("Usage:  python main.py <path-to-image-or-video>")
        print("Example:  python main.py samples/suspect_photo.jpg")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"🎯  Target file: {file_path}")
    print(f"🐝  Deploying Veritas Swarm …\n{DIVIDER}\n")

    # ── Run the swarm ───────────────────────────────────────────────────
    result = VeritasCrew(file_path).run()

    # ── Print final verdict ─────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("⚖️   F I N A L   V E R D I C T")
    print(DIVIDER)
    print(result)
    print(DIVIDER)


if __name__ == "__main__":
    main()
