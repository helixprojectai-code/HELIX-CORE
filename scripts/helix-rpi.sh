#!/bin/bash

set -euo pipefail # Exit immediately if a command exits with a non-zero status. Treat unset variables as an error. Prevent errors in a pipeline from being masked.

# --- Configuration Paths ---
MANIFEST_DIR="/home/aiadmin/helix-core-unified/thoughts/manifests"
LEDGER_MANIFEST="$MANIFEST_DIR/ledger_manifest.json"
L1_ANCHOR_TOOL="/home/aiadmin/helix-core-unified/scripts/l1_anchor_tool.py"
RESEARCH_DIR="/home/aiadmin/helix-core-unified/thoughts/research"
PLAN_DIR="/home/aiadmin/helix-core-unified/thoughts/plans"

# --- Function to find the newest RPI document (if no path is provided) ---
find_newest_rpi_doc() {
    local newest_file=""
    local newest_time=0

    # Check research directory
    for f in "$RESEARCH_DIR"/*.md; do
        if [[ -f "$f" ]]; then
            local f_time=$(stat -c %Y "$f") # Get last modification time
            if (( f_time > newest_time )); then
                newest_time=$f_time
                newest_file="$f"
            fi
        fi
    done

    # Check plan directory
    for f in "$PLAN_DIR"/*.md; do
        if [[ -f "$f" ]]; then
            local f_time=$(stat -c %Y "$f") # Get last modification time
            if (( f_time > newest_time )); then
                newest_time=$f_time
                newest_file="$f"
            fi
        fi
    done
    echo "$newest_file"
}

# --- Determine target file path based on argument or by finding newest ---
RPI_DOC_PATH=""
if [[ -n "$1" ]]; then # If an argument is provided, use it as the file path
    RPI_DOC_PATH="$1"
else # Otherwise, search for the newest .md file
    echo "[Helix-RPI] No file path provided. Searching for the newest RPI document in '$RESEARCH_DIR' and '$PLAN_DIR'..."
    RPI_DOC_PATH=$(find_newest_rpi_doc)
    if [[ -z "$RPI_DOC_PATH" ]]; then
        echo "Error: No RPI document found. Please provide a path or ensure documents exist in 'thoughts/research/' or 'thoughts/plans/'."
        exit 1
    fi
    echo "[Helix-RPI] Found newest document: '$RPI_DOC_PATH'"
fi

# --- Validate the determined RPI document file ---
if [[ ! -f "$RPI_DOC_PATH" ]]; then
    echo "Error: Document '$RPI_DOC_PATH' not found."
    exit 1
fi
if [[ "${RPI_DOC_PATH##*.}" != "md" ]]; then # Check if file extension is .md
    echo "Error: Document '$RPI_DOC_PATH' is not a Markdown (.md) file. Only Markdown files are processed."
    exit 1
fi

echo "[Helix-RPI] Processing document: '$RPI_DOC_PATH'"

# --- Generate SHA-256 hash of the RPI document ---
DOC_HASH=$(sha256sum "$RPI_DOC_PATH" | awk '{print $1}')
echo "[Helix-RPI] RPI Document SHA-256 Hash: $DOC_HASH"

# --- Prepare and Update Ledger Manifest (JSON) ---
TIMESTAMP_UTC=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
RELATIVE_PATH="${RPI_DOC_PATH##*/helix-core-unified/}" # Get path relative to helix-core-unified root

DOC_TYPE="RPI_DOCUMENT" # Default type
if [[ "$RPI_DOC_PATH" == *"/thoughts/research/"* ]]; then
    DOC_TYPE="RPI_RESEARCH"
elif [[ "$RPI_DOC_PATH" == *"/thoughts/plans/"* ]]; then
    DOC_TYPE="RPI_PLAN"
fi

# Initialize or load ledger_manifest.json
if [[ ! -f "$LEDGER_MANIFEST" ]]; then
    echo "[Helix-RPI] Creating new ledger manifest: '$LEDGER_MANIFEST'"
    cat <<EOF > "$LEDGER_MANIFEST"
    {
        "manifest_version": "1.0.0",
        "manifest_timestamp_utc": "$TIMESTAMP_UTC",
        "ledger_period_start_utc": "$TIMESTAMP_UTC",
        "ledger_period_end_utc": "$TIMESTAMP_UTC",
        "transactions": []
    }
EOF
fi

# Check if this exact document hash is already in the manifest to avoid duplicates
if jq --arg hash "$DOC_HASH" '.transactions[] | select(.file_hash_sha256 == $hash)' "$LEDGER_MANIFEST" | grep -q .; then
    echo "[Helix-RPI] Warning: Document with hash '$DOC_HASH' already found in manifest. Skipping addition."
else
    # Add new entry to the transactions array and update manifest timestamps using jq
    jq --arg ts "$TIMESTAMP_UTC" \
       --arg type "$DOC_TYPE" \
       --arg path "$RELATIVE_PATH" \
       --arg hash "$DOC_HASH" \
       '.transactions += [{
           "timestamp_utc": $ts,
           "type": $type,
           "filepath": $path,
           "file_hash_sha256": $hash
       }] | .manifest_timestamp_utc = $ts | .ledger_period_end_utc = $ts' \
       "$LEDGER_MANIFEST" > "${LEDGER_MANIFEST}.tmp" && mv "${LEDGER_MANIFEST}.tmp" "$LEDGER_MANIFEST"

    echo "[Helix-RPI] Updated manifest with RPI document details: '$LEDGER_MANIFEST'"
fi


# --- Generate SHA-256 hash of the updated manifest ---
MANIFEST_HASH=$(sha256sum "$LEDGER_MANIFEST" | awk '{print $1}')
echo "[Helix-RPI] Updated Manifest SHA-256 Hash: $MANIFEST_HASH"

# --- Human-Gated L1 Anchoring Command ---
echo ""
echo "--- L1 ANCHORING REQUIRED ---"
echo "The updated manifest has been hashed ('$MANIFEST_HASH')."
echo "To immutably anchor this manifest to Bitcoin Layer 1 (requires human confirmation for private key access),"
echo "please manually execute the following command:"
echo ""
echo "    python3 '$L1_ANCHOR_TOOL' '$MANIFEST_HASH'"
echo ""
echo "After successful execution, verify the transaction details in 'L1_ANCHOR_LOG.md'."
echo "-----------------------------"
