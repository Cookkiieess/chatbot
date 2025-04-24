import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyBmqN5tc4-tGoGIfMFy2n55MxCSBljO0gM")

# Initialize the Gemini Pro model
model = genai.GenerativeModel("gemini-1.5-pro-001")

def send_input(_text):
# Start a persistent chat session
    chat = model.start_chat(history=[])

    print("Gemini Chatbot is ready! (type 'exit' to quit)\n")

    while True:
        if _text.lower() == "exit":
            break

        response = chat.send_message(_text)
        print("Gemini:", response.text)
