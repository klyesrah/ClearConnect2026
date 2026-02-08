import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please say something...")
    audio = r.listen(source)
   
   
    print("Audio captured!")