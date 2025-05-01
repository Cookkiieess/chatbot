from stt import listen_and_transcribe
from local_model import send_input

#for wake call (examples)
key_word = ["hey spark-v", "hey sparkv", "sparkv", "spark-v", "Okay Google", "okay google", "Okay google"]

#listening for audio
while True:
        try:
            text = listen_and_transcribe()
            if text != "":
                print(f"you: {text}")
                for keyword in key_word:
                    if keyword in text:
                        print("entering second while loop...")
                        while True:
                            text_true = listen_and_transcribe()
                            if text_true != "":
                                print(f"you: {text_true}")
                                if "goodbye" in text_true.lower():
                                    send_input(text_true)
                                    print("exiting second while loop...")
                                    break
                                else:
                                    send_input(text_true)
                
        except sr.WaitTimeoutError:
            print("No speech detected. Try again...")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

