import pyttsx3
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip
import tempfile

def audioClip(text,voice:int=0):
    #Change voice to 1 for female voice

    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    # Set the ID of the desired voice
    # In this example, we are selecting the first voice from the list

    # Get the list of available voices
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)

    engine.setProperty("rate", 150) # Speed of the speech in words per minute
    engine.setProperty("volume", 1) # Volume of the speech (0 to 1)

    # Convert text to speech
    
    #engine.say(text)
    #engine.save_to_file(text,file)
    file = tempfile.NamedTemporaryFile(delete=False).name
    fileName,extension=os.path.splitext(file)
    fileName = fileName + ".mp3"
    print(fileName)
    engine.save_to_file(text,fileName)
    engine.runAndWait()
    audio_clip = AudioFileClip(fileName)
    return audio_clip