
#!/bin/bash

pip install -r requirements.txt
python3 main.py

# Define variables for file and folder paths
file_to_move="sales.env"
destination_folder="`~sales/"

mv "$file_to_move" ".env"

# Use mv command to move the file
mv "$file_to_move" "$destination_folder"

