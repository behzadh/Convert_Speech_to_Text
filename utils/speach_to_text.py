import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

class SpeechtoText:
    def __init__(self) -> None:
        self.recog = sr.Recognizer()
        self.path_short = '/Users/behzad/My_codings/Convert_Speech_to_Text/raw_data/speech_long.wav'

    def convert_speech(self):
        '''
        This function will convert recorded speech to text
        '''
        with sr.AudioFile(self.path_short) as source:
            # listen for the data (load audio to memory)
            audio_data = self.recog.record(source)
            # recognize (convert from speech to text)
            text = self.recog.recognize_google(audio_data)
            print(text)
        return text
    
    def long_speech(self):
        '''
        This function will convert long recorded speech to text
        '''
        pass

if __name__ == '__main__':
    speach = SpeechtoText()
    speach.convert_speech()