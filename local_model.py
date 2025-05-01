import requests
import tts

# API endpoint
url = "http://localhost:11434/api/generate"

def send_input(text):
# Request data (adjust model/prompt as needed)
# Doesnt work as required
    words = ["detail", "detailed"]
    for word in words:
        if word in text:
            data = {
                "model": "mistral",
                "prompt": f"{text}",
                "stream": False  # Set to True for streaming responses
            }
        else:
            data = {
                "model": "mistral",
                "prompt": f"provide a very short response to this: {text}",
                "stream": False  # Set to True for streaming responses
            }

# Send POST request
    response = requests.post(url, json=data)

# Print response
    if response.status_code == 200:
        response_f = response.json()["response"]
        tts.convert_tts(response_f)
    else:
        print("Error:", response.text)