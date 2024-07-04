import requests

def LoadResume():
    # Replace this URL with the URL of your deployed web app
    web_app_url = "https://digitalresume-sc.streamlit.app/"
    response = requests.get(web_app_url)

    if response.status_code == 200:
        print("Successfully saved to Google Drive")
        return response
    else:
        print("Failed to save the recept! ")
        return None

LoadResume()