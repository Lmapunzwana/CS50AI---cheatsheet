#!/bin/bash

BASE_SLUG="ai50/projects/2024/x"

# Loop through all week folders
for week in WEEK*/; do
    #loop through all subfolders
    for sub in "$week"*/ do
	subfolder=$(basename "$sub")

	echo "Submitting $subfolder -> $BASE_SLUG/$subfolder"
	cd "$sub" || { echo "Failed to enter $sub"; continue; }

	submit50 "$BASE_SLUG/$subfolder"

	cd - >/dev/null
	done
    done
