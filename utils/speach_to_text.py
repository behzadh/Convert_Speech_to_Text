import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import webbrowser as wb

class SpeechtoText:
    def __init__(self, speech_duration = 5) -> None:
        self.recog = sr.Recognizer()
        self.path = '/Users/behzad/My_codings/Convert_Speech_to_Text/raw_data/speech_long.wav'
        self.speech_duration = speech_duration #seconds

    def convert_speech(self):
        '''
        This function will convert recorded speech to text
        '''
        with sr.AudioFile(self.path) as source:
            audio_data = self.recog.record(source) # listen for the data (load audio to memory)
            text = self.recog.recognize_google(audio_data)
            print(text)
        return text
    
    def convert_speech_in_chunks(self, min_sil_len = 500, keep_sil = 1000):
        '''
        This function will convert recorded speech to text in multiple chunks
        '''
        sound = AudioSegment.from_wav(self.path)  
        # split audio sound where silence is n miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            min_silence_len = min_sil_len,
            silence_thresh = sound.dBFS-14,
            keep_silence = keep_sil, # keep the silence for n miliseconds
        )
        folder_name = "../raw_data/"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = self.recog.record(source)
                try:
                    text = self.recog.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error: ", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text
        return whole_text
    
    def live_speech_to_text(self):
        '''
        This function will use a mic to convert a user speech to text
        '''
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            self.recog.adjust_for_ambient_noise(source) 
            print(f'Start recording for {self.speech_duration} seconds...')
            audio_data = self.recog.record(source, duration=self.speech_duration)
            try:
                text = self.recog.recognize_google(audio_data,language='en-UK')
                print(f'You said: {text}')
            except:
                text = 'Null'
                print("Couldn't hear you")
        return text

if __name__ == '__main__':
    speach = SpeechtoText(6)
    speach.live_speech_to_text()