#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <csv_file>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

echo "Top 5 Most Active Users:"
echo "------------------------"

python3 -c "
import csv, sys
with open(sys.argv[1], encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['Username'])
" "$FILE" | sort | uniq -c | sort -nr | head -n 5
