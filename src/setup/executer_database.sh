#!/bin/bash

# Directory where the text files are initially located
SOURCE_DIR=../../data/text

# Directory where the text files should be moved to
TARGET_DIR=../../data/

echo "Starting script execution at $(date)"

# Step 1: Iterate over each .txt file in the source directory
for file in "$SOURCE_DIR"/*.txt; do
    echo "Processing file: $file"
    # Check if the file exists to prevent errors
    if [[ -f "$file" ]]; then
        echo "Deleting any files in $TARGET_DIR"
        # First, delete any files in the /data directory
        rm -rf "$TARGET_DIR"/*

        # Move the current .txt file to the /data directory
        echo "Moving $file to $TARGET_DIR"
        cp "$file" "$TARGET_DIR"

        # Step 2: Execute the command "python db_build.py"
        echo "Running db_build.py"
        python db_build.py

        echo "$file" | tee -a ../../results/results.txt
        echo "Processing questions.txt and running main.py for each line"
        # Step 3 and 4: Read from questions.txt and process each line
        while IFS= read -r line; do
            echo "Processing line: $line"
            # Execute "python main.py" with the line as input parameter and append output to results.txt
            python main.py "$line" >> ../../results/results.txt
        done < "../../results/questions.txt"

        # We move to the next file
    fi
done
echo "Script execution finished at $(date)"
