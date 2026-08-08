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


# Anthropic documents effort on a closed list of models, and Haiku 4.5 —
# the model every check-in runs on — is NOT on it. Passing the parameter
# anyway is at best ignored and at worst a 400 that kills the session, so
# the caller asks first rather than sending it blind.
# https://platform.claude.com/docs/en/build-with-claude/effort
_EFFORT_MODELS = frozenset((
    "claude-fable-5", "claude-mythos-5", "claude-mythos-preview",
    "claude-opus-5", "claude-opus-4-8", "claude-opus-4-7", "claude-opus-4-6",
    "claude-opus-4-5-20251101", "claude-sonnet-5", "claude-sonnet-4-6",
))


def supports_effort(model: str | None) -> bool:
    """Whether this model accepts the effort parameter at all."""
    if not model:
        return False
    name = model.split("/")[-1]
    # Bedrock ids look like us.anthropic.claude-sonnet-5-v1:0
    for known in _EFFORT_MODELS:
        if name == known or known in name:
            return True
    return False


def session_kwargs(model: str | None, effort: str | None) -> dict:
    """Options that depend on which model is actually running, ready to
    splat into ClaudeAgentOptions."""
    kw: dict = {"model": resolve(model)}
    if effort and supports_effort(model):
        kw["effort"] = effort
    return kw


def describe() -> str:
    if not using_bedrock():
        return "Anthropic API (direct)"
    region = os.environ.get("AWS_REGION", "unset-region")
    return f"Amazon Bedrock ({region})"
