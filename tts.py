from gtts import gTTS
import os
import base64

def generate_audio_base64(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = "temp_verdict.mp3"
        tts.save(temp_file)
        
        with open(temp_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
        os.remove(temp_file)
        return b64
    except Exception as e:
        return None
