from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def convert_tts(text):
    # Generate speech in memory
    mp3_fp = BytesIO()
    tts = gTTS(f"{text}", lang='en')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Play using pydub
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    play(audio)