"""
Veritas Swarm — Task Definitions
4 parallel analysis tasks + 1 blocking master verdict task.
"""

from crewai import Task


def create_tasks(agents: dict, file_path: str):
    """
    Build analysis tasks based on available agents.
    
    The orchestrator may provide a subset of agents based on file type.
    Only create tasks for agents that are present in the agents dict.
    The Master Verdict task always runs, with context set to available tasks.
    """
    tasks = []
    
    # Only create tasks for agents that are present
    if "biometric_sentinel" in agents:
        biometric_task = Task(
            description=(
                f"Analyse the following media file for biometric anomalies:\\n"
                f"  File: {file_path}\\n\\n"
                "CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.\\n"
                "Execute these tools in order:\\n"
                "1. analyze_facial_landmarks - Detect facial geometry anomalies and tracking consistency\\n"
                "2. detect_blink_anomalies - Measure blink rate and detect unnatural patterns\\n"
                "3. detect_face_blending - Scan for face-swap paste boundaries\\n\\n"
                "Additional focus areas (if observable from tool outputs):\\n"
                "• Eye-glint consistency (position, shape, count)\\n"
                "• Remote PPG (rPPG) pulse signal presence\\n"
                "• Skin micro-texture under magnification\\n"
                "• Pupil dilation / iris boundary irregularities\\n\\n"
                "Report each finding with a confidence tag: HIGH / MEDIUM / LOW.\\n"
                "Include specific metrics from tool outputs (e.g., 'Blink rate: 3.2/min, Normal: 15-20/min')."
            ),
            expected_output=(
                "A structured forensic report listing each biometric indicator "
                "checked, whether it passed or failed, the confidence level, "
                "and a short justification for each finding."
            ),
            agent=agents["biometric_sentinel"],
            async_execution=False,
        )
        tasks.append(biometric_task)

    if "physics_inspector" in agents:
        physics_task = Task(
            description=(
                f"Analyse the following media file for physics & lighting anomalies:\\n"
                f"  File: {file_path}\\n\\n"
                "CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.\\n"
                "Execute these tools in order:\\n"
                "1. analyze_head_pose_3d - Calculate 3D head rotation and detect unnatural movements\\n"
                "2. detect_lighting_inconsistencies - Analyze shadow vectors and lighting coherence\\n\\n"
                "Additional focus areas (if observable from tool outputs):\\n"
                "• Shadow geometry and ground-truth plausibility\\n"
                "• Specular highlight coherence on skin, eyes, and glossy surfaces\\n"
                "• Reflection accuracy in eyes and mirrors\\n"
                "• Colour temperature consistency across the scene\\n\\n"
                "Report each finding with a confidence tag: HIGH / MEDIUM / LOW.\\n"
                "Include specific metrics from tool outputs (e.g., 'Sudden movements: 12, Lighting inconsistencies: 35%')."
            ),
            expected_output=(
                "A structured forensic report listing each physics/lighting "
                "indicator checked, whether it passed or failed, the confidence "
                "level, and a short justification for each finding."
            ),
            agent=agents["physics_inspector"],
            async_execution=False,
        )
        tasks.append(physics_task)

    if "signal_analyst" in agents:
        signal_task = Task(
            description=(
                f"Analyse the following media file for digital manipulation artefacts:\\n"
                f"  File: {file_path}\\n\\n"
                "CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.\\n"
                "Execute these tools in order:\\n"
                "1. analyze_frequency_domain - Perform FFT analysis to detect high-frequency GAN fingerprints\\n"
                "2. detect_gan_fingerprints - Detect checkerboard artifacts from GAN upsampling\\n\\n"
                "Additional focus areas (if observable from tool outputs):\\n"
                "• GAN-induced spatial warping or geometric distortion\\n"
                "• Blending seams between face region and background\\n"
                "• Abnormal pixel noise distribution patterns\\n"
                "• JPEG / H.264 re-compression ghosts or double-quantisation\\n\\n"
                "Report each finding with a confidence tag: HIGH / MEDIUM / LOW.\\n"
                "Include specific metrics from tool outputs (e.g., 'High-freq ratio: 0.28, Normal: 0.05-0.15')."
            ),
            expected_output=(
                "A structured forensic report listing each digital-signal "
                "indicator checked, whether it passed or failed, the confidence "
                "level, and a short justification for each finding."
            ),
            agent=agents["signal_analyst"],
            async_execution=False,
        )
        tasks.append(signal_task)

    if "sync_specialist" in agents:
        sync_task = Task(
            description=(
                f"Analyse the following media file for audio-visual sync anomalies:\\n"
                f"  File: {file_path}\\n\\n"
                "CRITICAL: You MUST use your specialized analysis tools to perform comprehensive analysis.\\n"
                "Execute these tools in order:\\n"
                "1. extract_audio_track - Extract audio from video for analysis\\n"
                "2. analyze_lip_sync - Track mouth movements and detect speech patterns\\n"
                "3. calculate_av_offset - Measure audio-visual synchronization offset\\n\\n"
                "If the file is a still image with no audio, note that audio-visual "
                "sync checks are not applicable and report accordingly.\\n\\n"
                "Additional focus areas (if observable from tool outputs):\\n"
                "• Natural speech cadence and rhythm\\n"
                "• Room acoustic fingerprint vs. visual environment\\n"
                "• TTS (text-to-speech) artefacts in the audio track\\n\\n"
                "Report each finding with a confidence tag: HIGH / MEDIUM / LOW.\\n"
                "Include specific metrics from tool outputs (e.g., 'MAR variation: 0.008, Offset: 0ms')."
            ),
            expected_output=(
                "A structured forensic report listing each audio-visual sync "
                "indicator checked, whether it passed or failed / was not applicable, "
                "the confidence level, and a short justification."
            ),
            agent=agents["sync_specialist"],
            async_execution=False,
        )
        tasks.append(sync_task)

    # Chief Justice always runs, with context set to available tasks
    master_verdict = Task(
        description=(
            "You are the Chief Justice of the Veritas Swarm. You have received "
            "forensic reports from specialist agents who independently "
            "analysed the same media file. Your job:\\n\\n"
            "1. Read ALL reports carefully.\\n"
            "2. Weigh the evidence — resolve any conflicting signals.\\n"
            "3. Produce a single VERDICT SCORE from 0 (certainly real) to "
            "   100 (certainly fake).\\n"
            "4. State your CONFIDENCE level: HIGH / MEDIUM / LOW.\\n"
            "5. List KEY FINDINGS as bullet points.\\n"
            "6. Write a LAYMAN'S BRIEF — a short, non-technical paragraph "
            "   explaining the 'Tell' (why it looks fake or real) so that "
            "   any regular person can understand it.\\n\\n"
            "Be decisive. Hedge only when the evidence is genuinely ambiguous."
        ),
        expected_output=(
            "VERDICT SCORE: <0-100>\\n"
            "CONFIDENCE: <HIGH | MEDIUM | LOW>\\n\\n"
            "KEY FINDINGS:\\n"
            "• <finding 1>\\n"
            "• <finding 2>\\n"
            "• ...\\n\\n"
            "LAYMAN'S BRIEF:\\n"
            "<A plain-English paragraph explaining the 'Tell' — why the media "
            "is likely real or fake, written for a non-technical audience.>"
        ),
        agent=agents["chief_justice"],
        context=tasks,  # Context = all available specialist tasks
        async_execution=False,
    )

    return tasks + [master_verdict]
