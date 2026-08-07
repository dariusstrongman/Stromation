"""The voice of the documentary.

Turns a narration script into a real mp3 via ElevenLabs and parks it in
Supabase Storage, so an episode can be watched — and recorded — with sound.
Owner's media cost, never the founder's: it uses STRO_MEDIA_* credentials
which are deliberately absent from the founder's briefing. He does not know
he is being filmed.
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


def voice_narration(narration: dict) -> str | None:
    """Give a narration row its voice. Returns the audio URL, or None."""
    key = os.environ.get("STRO_MEDIA_ELEVENLABS_KEY")
    if not key or not narration:
        return None
    audio = _tts(narration["script"], key)
    if not audio:
        return None
    url = _upload(audio, f"day-{narration.get('day') or 0}-{narration['id']}.mp3")
    if url:
        company.update("narrations", narration["id"], {"audio_url": url})
    return url
