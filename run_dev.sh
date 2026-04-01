#!/bin/bash

set -a
source "$(dirname "$0")/.env"
set +a

for arg in "$@"; do
    if [ "$arg" = "--dev" ] || [ "$arg" = "-d" ]; then
        export DEV_MODE=1
        break
    fi
done

output_file="log.txt"

echo "" >> "$output_file"

date "+%Y-%m-%d %H:%M:%S" >> "$output_file"

python src/main.py "$@" 2>&1 | tee -a log.txt
