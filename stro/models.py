"""Where inference is bought.

The runtime speaks to Anthropic directly or through Amazon Bedrock,
decided entirely by environment. Bedrock is the intended long-term path:
inference is the dominant variable cost of an autonomous company, and AWS
credits are redeemable against it.

Model names in the database stay human ("claude-sonnet-5"). Bedrock wants
its own identifiers, so the mapping lives here and is overridable by env —
Bedrock IDs change and are region-dependent, and a wrong one hard-fails
every session, which is not something to hardcode.
"""
import json
import os

# Sensible defaults; override wholesale with STRO_BEDROCK_MODEL_MAP, which
# must be a JSON object of {friendly_name: bedrock_id}.
_DEFAULT_MAP = {
    "claude-opus-5": "us.anthropic.claude-opus-5-v1:0",
    "claude-sonnet-5": "us.anthropic.claude-sonnet-5-v1:0",
    "claude-haiku-4-5-20251001": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
}


def using_bedrock() -> bool:
    return os.environ.get("CLAUDE_CODE_USE_BEDROCK", "").strip() in ("1", "true")


def _map() -> dict:
    raw = os.environ.get("STRO_BEDROCK_MODEL_MAP")
    if raw:
        try:
            return {**_DEFAULT_MAP, **json.loads(raw)}
        except Exception as exc:  # noqa: BLE001
            print(f"[models] bad STRO_BEDROCK_MODEL_MAP, using defaults: {exc!r}")
    return _DEFAULT_MAP


def resolve(model: str | None) -> str | None:
    """The identifier the runtime should actually ask for."""
    if not model or not using_bedrock():
        return model
    m = _map()
    if model in m:
        return m[model]
    if model.startswith(("us.", "eu.", "apac.", "anthropic.")):
        return model          # already a Bedrock id
    print(f"[models] no Bedrock mapping for {model!r}; passing through")
    return model


def describe() -> str:
    if not using_bedrock():
        return "Anthropic API (direct)"
    region = os.environ.get("AWS_REGION", "unset-region")
    return f"Amazon Bedrock ({region})"
