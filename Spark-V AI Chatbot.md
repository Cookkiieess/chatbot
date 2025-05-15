## 🎯 Overview
**Spark-V** is a voice-activated personal assistant that:
- Uses `faster-whisper` for fast, accurate **speech-to-text (STT)**
- Uses `gTTS` + `pydub` for realistic **text-to-speech (TTS)**
- Connects to a **local LLM (Mistral)** for offline AI responses
- Listens for wake words like "Hey Spark-V" and responds conversationally

---

## 📁 Project Structure

| File            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `main.py`       | Main entry point; handles wake-word detection, recording, and model logic   |
| `stt.py`        | Converts voice input to text using `faster-whisper`                         |
| `tts.py`        | Converts model responses to voice using `gTTS` and plays it with `pydub`    |
| `local_model.py`| Sends prompts to a local LLM API (Mistral) and handles response playback    |
| `face.py`       | (GUI for animated emotion eyes — *not used in Spark-V*)                     |

---

## 🔁 Flow of Execution

1. **Wake Word Detection**
   - Waits for phrases like `"hey spark-v"` or `"okay google"` (defined in `stt.py`)

2. **Command Capture**
   - On wake word, starts listening again for user’s actual input
   - Passes command to `local_model.send_input()`

3. **Local LLM Interaction**
   - Sends input to a local Mistral API via POST request
   - Chooses detailed or short responses depending on prompt content

4. **TTS Playback**
   - Uses `gTTS` to synthesize response speech
   - Plays audio with `pydub`

---

## 🧠 Features

- ✅ Wake-word detection
- 🗣️ Fast, local speech-to-text with Whisper
- 🤖 Local-only response generation via Mistral
- 🔈 TTS response output

---

## ⚙️ Configuration

- Whisper model set to `"tiny"` for speed
- `energy_threshold` and `pause_threshold` tuned for noise control
- Mistral server expected at `http://localhost:11434`

---

## 🚧 Known Issues

- Basic error handling in API requests and speech playback
- No long-term memory yet (can be added)
- Conditional response logic in `local_model.py` is basic

---

## ▶️ Run Instructions

```bash
# Start the Mistral server (Ollama or equivalent)
# Then run the assistant:
python main.py
```

Say: `Hey Spark-V`, then speak your command.

---

## 📌 To-Do (Suggestions)

- Add persistent memory (JSON or vector DB)
- Improve prompt routing in `local_model.py`
- Add command history or logs