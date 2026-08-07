# Stro's body: one container, woken by Railway cron. Each run = one session.
FROM node:22-slim

# Claude Code CLI (the Agent SDK drives it) + python runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip git curl ca-certificates ripgrep \
        espeak-ng ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @anthropic-ai/claude-code

WORKDIR /app
COPY stro/requirements.txt stro/requirements.txt
RUN pip3 install --break-system-packages -r stro/requirements.txt
# Kokoro: the documentary voice, self-hosted and free forever. Model files
# are baked into the image — the container is disposable, so a runtime
# download would repeat on every single session.
ENV KOKORO_DIR=/opt/kokoro
RUN mkdir -p $KOKORO_DIR \
    && curl -sSL -o $KOKORO_DIR/kokoro-v1.0.onnx \
       https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx \
    && curl -sSL -o $KOKORO_DIR/voices-v1.0.bin \
       https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

COPY stro/ stro/

# Claude Code refuses to run permission-free as root and needs a writable
# HOME for its config; give the founder a real user and his own home.
RUN useradd -m -u 10001 stro \
    && mkdir -p /workspace \
    && chown -R stro:stro /workspace /app
USER stro
ENV HOME=/home/stro \
    STRO_HOME=/home/stro \
    STRO_WORKSPACE=/workspace \
    IS_SANDBOX=1

CMD ["python3", "-m", "stro.main"]
