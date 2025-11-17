#!/bin/bash

# Get directory where this script is located
SCIPTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load configuration safely
USER="$(<"$SCIPTPATH/sync-conf.d/USERNAME")"
HOST="$(<"$SCIPTPATH/sync-conf.d/HOST")"
REMOTE_DIR="$(<"$SCIPTPATH/sync-conf.d/REMOTE_DIR")"

# Watch all files recursively in the project folder
find "$SCIPTPATH" -type f | entr -r rsync -avz --delete "$SCIPTPATH"/ "${USER}@${HOST}:${REMOTE_DIR}"

