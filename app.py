import asyncio
import io
import tempfile
import os
import streamlit as st
import edge_tts

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Audify — Text to Speech",
    page_icon="🎙️",
    layout="centered",
)

# ─── Styling ──────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Light background */
.stApp {
    background-color: #faf9f7;
    color: #1a1a1a;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 740px; }

/* Hero title */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.05;
    color: #1a1a1a;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-title em {
    font-style: italic;
    color: #b07d4a;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1.05rem;
    color: #888078;
    margin-top: 0.6rem;
    letter-spacing: 0.01em;
}
.divider {
    border: none;
    border-top: 1px solid #e8e4de;
    margin: 2rem 0;
}

/* Section labels */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b0a89e;
    margin-bottom: 0.5rem;
}

/* Input area */
.stTextArea textarea {
    background-color: #ffffff !important;
    border: 1.5px solid #e0dbd4 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stTextArea textarea:focus {
    border-color: #b07d4a !important;
    box-shadow: 0 0 0 3px rgba(176,125,74,0.1) !important;
}
.stTextArea textarea::placeholder {
    color: #c0b8b0 !important;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background-color: #ffffff !important;
    border: 1.5px dashed #d8d2ca !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #b07d4a !important;
    background-color: #fdf6ef !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 1.5px solid #e0dbd4 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    padding: 0 !important;
}
.stSlider [data-baseweb="thumb"] {
    background-color: #b07d4a !important;
    border-color: #b07d4a !important;
}
.stSlider [data-baseweb="track-fill"] {
    background-color: #b07d4a !important;
}
.stSlider [data-baseweb="track"] {
    background-color: #e8e4de !important;
}

/* Labels */
.stSelectbox label, .stSlider label {
    color: #555050 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
}

/* Convert button */
.stButton > button {
    background-color: #1a1a1a !important;
    color: #faf9f7 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
}
.stButton > button:hover {
    background-color: #b07d4a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(176,125,74,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
.stButton > button:disabled {
    background-color: #d8d2ca !important;
    color: #a09890 !important;
    box-shadow: none !important;
}

/* Audio player */
audio {
    width: 100%;
    border-radius: 8px;
    margin-top: 0.5rem;
}

/* Stats row */
.stat-row {
    display: flex;
    gap: 2rem;
    margin-top: 0.5rem;
}
.stat-item {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #a09890;
}
.stat-item span {
    color: #b07d4a;
    font-weight: 500;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-bottom: 1.5px solid #e8e4de !important;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #b0a89e !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.5rem 1.2rem !important;
    transition: color 0.2s;
}
.stTabs [aria-selected="true"] {
    color: #1a1a1a !important;
    border-bottom-color: #b07d4a !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    border: 1.5px solid #e0dbd4 !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
.stDownloadButton > button:hover {
    border-color: #b07d4a !important;
    color: #b07d4a !important;
    background-color: #fdf6ef !important;
}

/* Success / warning / error */
.stSuccess {
    background-color: #f0f8f0 !important;
    border: 1px solid #c8e6c8 !important;
    border-radius: 8px !important;
    color: #3a7a3a !important;
}
.stWarning {
    background-color: #fdf8f0 !important;
    border: 1px solid #f0deb8 !important;
    border-radius: 8px !important;
}
.stError {
    background-color: #fdf0f0 !important;
    border: 1px solid #f0c8c8 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Voice Definitions ────────────────────────────────────────────────────────

VOICES = {
    "Emma — Female, Natural"     : "en-US-EmmaNeural",
    "Aria — Female, Expressive"  : "en-US-AriaNeural",
    "Jenny — Female, Friendly"   : "en-US-JennyNeural",
    "Michelle — Female, Warm"    : "en-US-MichelleNeural",
    "Guy — Male, Professional"   : "en-US-GuyNeural",
    "Andrew — Male, Warm"        : "en-US-AndrewNeural",
    "Brian — Male, Deep"         : "en-US-BrianNeural",
    "Ryan (en-GB) — Male, British": "en-GB-RyanNeural",
    "Sonia (en-GB) — Female, British": "en-GB-SoniaNeural",
}


# ─── TTS Core ─────────────────────────────────────────────────────────────────

async def synthesize(text: str, voice: str, rate: str) -> bytes:
    """Convert text to MP3 bytes in memory."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def run_tts(text: str, voice: str, rate: str) -> bytes:
    return asyncio.run(synthesize(text, voice, rate))


# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div>
  <p class="hero-title"><em>Audify</em></p>
  <p class="hero-sub">Turn any text into natural-sounding audio — paste, upload, convert.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─── Input ────────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">01 — Input</p>', unsafe_allow_html=True)

tab_paste, tab_upload = st.tabs(["PASTE TEXT", "UPLOAD .TXT"])

text_input = ""

with tab_paste:
    pasted = st.text_area(
        label="text",
        placeholder="Paste your text here — notes, articles, interview prep, anything...",
        height=220,
        label_visibility="collapsed",
    )
    if pasted.strip():
        text_input = pasted.strip()
        word_count = len(text_input.split())
        char_count = len(text_input)
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-item"><span>{word_count:,}</span> words</div>
            <div class="stat-item"><span>{char_count:,}</span> characters</div>
            <div class="stat-item">~<span>{max(1, round(word_count / 150))}</span> min audio</div>
        </div>
        """, unsafe_allow_html=True)

with tab_upload:
    uploaded = st.file_uploader(
        "Upload a .txt file",
        type=["txt"],
        label_visibility="collapsed",
    )
    if uploaded:
        try:
            file_text = uploaded.read().decode("utf-8").strip()
            if file_text:
                text_input = file_text
                word_count = len(text_input.split())
                char_count = len(text_input)
                st.markdown(f"""
                <div class="stat-row">
                    <div class="stat-item"><span>{uploaded.name}</span></div>
                    <div class="stat-item"><span>{word_count:,}</span> words</div>
                    <div class="stat-item">~<span>{max(1, round(word_count / 150))}</span> min audio</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("The uploaded file appears to be empty.")
        except UnicodeDecodeError:
            st.error("Could not read file — make sure it's a plain UTF-8 text file.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─── Settings ─────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">02 — Voice Settings</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    voice_label = st.selectbox(
        "Voice",
        options=list(VOICES.keys()),
        index=0,
        label_visibility="visible",
    )
    selected_voice = VOICES[voice_label]

with col2:
    rate_pct = st.slider(
        "Speaking Rate",
        min_value=-30,
        max_value=30,
        value=0,
        step=5,
        format="%d%%",
    )
    rate_str = f"{rate_pct:+d}%"

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─── Convert ──────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">03 — Generate</p>', unsafe_allow_html=True)

convert_btn = st.button("▶  Convert to MP3", disabled=not bool(text_input))

if convert_btn and text_input:
    with st.spinner("Synthesizing audio..."):
        try:
            mp3_bytes = run_tts(text_input, selected_voice, rate_str)

            st.success(f"Done — {len(mp3_bytes) / 1024:.0f} KB generated")

            st.audio(mp3_bytes, format="audio/mp3")

            # Derive a filename from the first few words
            slug = "_".join(text_input.split()[:4])
            slug = "".join(c if c.isalnum() or c == "_" else "" for c in slug).lower()
            filename = f"audify_{slug or 'audio'}.mp3"

            st.download_button(
                label="⬇  Download MP3",
                data=mp3_bytes,
                file_name=filename,
                mime="audio/mpeg",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Conversion failed: {e}")

elif convert_btn and not text_input:
    st.warning("Please paste some text or upload a .txt file first.")


# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #c0b8b0; text-align: center; letter-spacing: 0.08em; line-height: 2;">
POWERED BY MICROSOFT EDGE NEURAL TTS &nbsp;·&nbsp; NO API KEY REQUIRED &nbsp;·&nbsp; FREE
<br>
DEVELOPED BY &nbsp;<a href="https://github.com/s3achan" target="_blank" style="color: #b07d4a; text-decoration: none; letter-spacing: 0.08em;">s3achan</a>&nbsp; · &nbsp;<a href="https://github.com/s3achan/Audify---txt2mp3" target="_blank" style="color: #b07d4a; text-decoration: none; letter-spacing: 0.08em;">VIEW ON GITHUB ↗</a>
</p>
""", unsafe_allow_html=True)