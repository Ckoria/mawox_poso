import requests

def download_file_from_google_drive(shared_link, destination):
    # Extract file ID from the shared link
    file_id = shared_link.split('/d/')[1].split('/')[0]
    # Construct the URL to download the file
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    response = requests.get(download_url, stream=True)
    
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=32768):
                file.write(chunk)



