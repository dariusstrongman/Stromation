# Stro's body: one container, woken by Railway cron. Each run = one session.
FROM node:22-slim

# Claude Code CLI (the Agent SDK drives it) + python runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip git curl ca-certificates ripgrep \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @anthropic-ai/claude-code

WORKDIR /app
COPY stro/requirements.txt stro/requirements.txt
RUN pip3 install --break-system-packages -r stro/requirements.txt
COPY stro/ stro/

RUN mkdir -p /workspace
ENV STRO_WORKSPACE=/workspace

CMD ["python3", "-m", "stro.main"]
