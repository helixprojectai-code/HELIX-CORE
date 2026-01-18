#!/bin/bash

# Grounded Path
SITE_ROOT="/home/aiadmin/helix-core-unified"
LEDGER_MANIFEST="$SITE_ROOT/thoughts/manifests/ledger_manifest.json"
L1_ANCHOR_TOOL="$SITE_ROOT/scripts/l1_anchor_tool.py"

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_user_memory_file>"
    exit 1
fi

FILE_PATH="$1"
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found at $FILE_PATH"
    exit 1
fi

# 1. Generate Metadata
SHA256_HASH=$(sha256sum "$FILE_PATH" | awk '{print $1}')
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# 2. Update the Manifest Object
# This targets the '.transactions' array specifically.
tmp_file=$(mktemp)
jq --arg ts "$TIMESTAMP" \
   --arg path "$FILE_PATH" \
   --arg hash "$SHA256_HASH" \
   '.transactions += [{"timestamp_utc": $ts, "type": "VAULT_INGESTION", "filepath": $path, "file_hash_sha256": $hash}] | .manifest_timestamp_utc = $ts | .ledger_period_end_utc = $ts' \
   "$LEDGER_MANIFEST" > "$tmp_file" && mv "$tmp_file" "$LEDGER_MANIFEST"

echo "✅ Indexed: $SHA256_HASH"
echo "Anchor Command: python3 $L1_ANCHOR_TOOL $SHA256_HASH"
