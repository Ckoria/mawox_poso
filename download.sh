#!/bin/bash

# URL of the file to download from Google Drive
file_url= "https://drive.google.com/file/d/1_f_v7c133PzVKCG6SDsyVYYrFqCNZ6uc/view?usp=sharing"

# Destination path where the file will be saved
destination_path="/WTC-Projects/mawox_poso/sales/.env"

ls
# Download the file using gdown
gdown "$file_url" -O "$destination_path"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "File downloaded successfully to $destination_path"
else
    echo "Error: Failed to download file from Google Drive."
fi

