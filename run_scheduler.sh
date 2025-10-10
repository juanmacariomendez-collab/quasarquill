#!/usr/bin/env bash
set -euo pipefail
# random jitter up to 10 minutes
JITTER_MAX=1200
sleep $((RANDOM % JITTER_MAX))
set -a; [ -f "$HOME/.env" ] && . "$HOME/.env"; set +a
{
  echo "[$(date -Is)] DIAG: whoami=$(id -un) TOKEN_LEN=${#TELEGRAM_TOKEN} CHAT=${TELEGRAM_CHAT_ID:-<empty>}"
} >> /root/quasarquill/cron.log
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /root/quasarquill
/usr/bin/python3 -m auto_updater.scheduler >> /root/quasarquill/cron.log 2>&1
