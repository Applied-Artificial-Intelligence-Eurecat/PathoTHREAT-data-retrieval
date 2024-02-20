#!/bin/bash

# Target directory to search for .txt files
DIRECTORY="../../data/text"

# Iterate over all .txt files in the directory
for FILE in "$DIRECTORY"/*.txt; do
    # Check if the file exists and is a regular file
    if [ -f "$FILE" ]; then
        # Read the file content
        CONTENT=$(cat "$FILE")
        # Get the length of the content
        LENGTH=${#CONTENT}
        # Print the file name and its content length
        echo "File: $FILE - Length: $LENGTH characters"
    fi
done
