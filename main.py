import speech_recognition
r = speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    print("Please say something")
    audio = r.listen(source)


    print("Audio captured!")