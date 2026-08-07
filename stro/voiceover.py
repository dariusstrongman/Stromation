"""The voice of the documentary.

Kokoro runs inside the container: a small open-weights TTS model with a
proper British narrator voice, no API, no account, no per-episode cost. The
model files are baked into the image because the container is disposable —
downloading at runtime would repeat every session. ElevenLabs stays wired
as an optional upgrade if STRO_MEDIA_ELEVENLABS_KEY is set.

Owner's media cost, never the founder's: the STRO_MEDIA_* credentials are
deliberately absent from the founder's briefing. He does not know he is
being filmed.
"""
import json
import os
import urllib.error
import urllib.request

from . import company

# George — British, measured, documentary. Overridable per deployment.
DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"
BUCKET = "episodes"


def _tts(script: str, key: str) -> bytes | None:
    voice = os.environ.get("STRO_MEDIA_VOICE_ID", DEFAULT_VOICE)
    payload = {
        "text": script,
        "model_id": os.environ.get("STRO_MEDIA_TTS_MODEL",
                                   "eleven_multilingual_v2"),
        # Steady and unhurried: a naturalist, not an announcer.
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.75,
                           "style": 0.15, "use_speaker_boost": True},
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
        method="POST", data=json.dumps(payload).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except Exception:  # noqa: BLE001 — a silent episode beats a broken session
        return None


def _upload(audio: bytes, name: str) -> str | None:
    """Store the mp3 publicly and return its URL."""
    base = os.environ["SUPABASE_URL"].rstrip("/")
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        f"{base}/storage/v1/object/{BUCKET}/{name}", method="POST",
        data=audio,
        headers={"Authorization": f"Bearer {key}", "apikey": key,
                 "Content-Type": "audio/mpeg", "x-upsert": "true"})
    try:
        urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        if e.code not in (200, 201):
            return None
    except Exception:  # noqa: BLE001
        return None
    return f"{base}/storage/v1/object/public/{BUCKET}/{name}"


def _kokoro(script: str) -> bytes | None:
    """Synthesize locally, return mp3 bytes. Long scripts are spoken
    paragraph by paragraph and joined, which also gives the narration its
    natural breathing pauses."""
    import subprocess
    import tempfile
    try:
        import numpy as np
        import soundfile as sf
        from kokoro_onnx import Kokoro
    except Exception:  # noqa: BLE001 — image without the model
        return None
    d = os.environ.get("KOKORO_DIR", "/opt/kokoro")
    onnx, voices = f"{d}/kokoro-v1.0.onnx", f"{d}/voices-v1.0.bin"
    if not (os.path.exists(onnx) and os.path.exists(voices)):
        return None
    voice = os.environ.get("STRO_MEDIA_VOICE", "bm_george")
    try:
        k = Kokoro(onnx, voices)
        chunks, rate = [], 24000
        for para in [p.strip() for p in script.split("\n") if p.strip()]:
            samples, rate = k.create(para, voice=voice, speed=0.92,
                                     lang="en-gb")
            chunks.append(samples)
            chunks.append(np.zeros(int(rate * 0.55)))   # a beat between them
        if not chunks:
            return None
        audio = np.concatenate(chunks)
        with tempfile.TemporaryDirectory() as tmp:
            wav, mp3 = f"{tmp}/n.wav", f"{tmp}/n.mp3"
            sf.write(wav, audio, rate)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
                            "-codec:a", "libmp3lame", "-b:a", "128k", mp3],
                           check=True, timeout=180)
            with open(mp3, "rb") as f:
                return f.read()
    except Exception:  # noqa: BLE001 — a silent episode beats a broken session
        return None


def voice_narration(narration: dict) -> str | None:
    """Give a narration row its voice. Returns the audio URL, or None."""
    if not narration:
        return None
    # Free and local by default; ElevenLabs only if explicitly preferred.
    audio = None
    key = os.environ.get("STRO_MEDIA_ELEVENLABS_KEY")
    if key and os.environ.get("STRO_MEDIA_TTS") == "elevenlabs":
        audio = _tts(narration["script"], key)
    if audio is None:
        audio = _kokoro(narration["script"])
    if audio is None and key:
        audio = _tts(narration["script"], key)      # last resort
    if not audio:
        return None
    url = _upload(audio, f"day-{narration.get('day') or 0}-{narration['id']}.mp3")
    if url:
        company.update("narrations", narration["id"], {"audio_url": url})
    return url
