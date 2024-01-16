import base64

with open("alarm.wav", "rb") as audio_file:
    encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

with open("alarm_base64.txt", "w") as text_file:
    text_file.write(encoded_string)
