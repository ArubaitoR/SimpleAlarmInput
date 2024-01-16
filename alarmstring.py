import base64

with open("alarm.wav", "rb") as audio_file:
    encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')