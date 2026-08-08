#!/bin/sh
# Railway mounts the volume as root, but Claude Code refuses to run
# permission-free as root — so start as root only long enough to hand the
# workspace to the founder, then drop privileges for the actual session.
set -e
mkdir -p "${STRO_WORKSPACE:-/workspace}"
chown -R stro:stro "${STRO_WORKSPACE:-/workspace}" 2>/dev/null || true
exec setpriv --reuid=stro --regid=stro --init-groups "$@"
