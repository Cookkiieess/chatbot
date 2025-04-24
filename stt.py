from faster_whisper import WhisperModel
import speech_recognition as sr
import local_model


# Initialize faster-whisper model (choose size: tiny, base, small, medium, large-v2)
model = WhisperModel("tiny", device="cpu", compute_type="float32")  # Use "cuda" if GPU

# Initialize speech recognizer (for microphone)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 4000  # Default: 300 (higher = less sensitive)
recognizer.pause_threshold = 1.5    # Seconds of silence to stop (default: 0.8)


def transcribe_audio(audio_file):
    """Transcribe audio using faster-whisper"""
    segments, _ = model.transcribe(audio_file, beam_size=5)
    transcription = " ".join(segment.text for segment in segments)
    return transcription

def listen_and_transcribe():
    """Listen to microphone and transcribe using faster-whisper"""
    with microphone as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Speak now (waiting for speech)...")
        audio = recognizer.listen(source)
    
    # Save audio to a temporary file (Whisper requires a file)
    temp_audio = "temp_audio.wav"
    with open(temp_audio, "wb") as f:
        f.write(audio.get_wav_data())
    
    # Transcribe using faster-whisper
    transcription = transcribe_audio(temp_audio)
    return transcription
    
key_word = ["hey spark-v", "hey sparkv", "sparkv", "spark-v", "Okay Google", "okay google", "Okay google"]

if __name__ == "__main__":
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
                                    local_model.send_input(text_true)
                                    print("exiting second while loop...")
                                    break
                                else:
                                    local_model.send_input(text_true)
                
        except sr.WaitTimeoutError:
            print("No speech detected. Try again...")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
