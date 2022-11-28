import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

class SpeechtoText:
    def __init__(self) -> None:
        self.recog = sr.Recognizer()
        self.path = '/Users/behzad/My_codings/Convert_Speech_to_Text/raw_data/speech_long.wav'

    def convert_speech(self):
        '''
        This function will convert recorded speech to text
        '''
        with sr.AudioFile(self.path) as source:
            audio_data = self.recog.record(source) # listen for the data (load audio to memory)
            text = self.recog.recognize_google(audio_data)
            print(text)
        return text
    
    def convert_speech_in_chunks(self):
        '''
        This function will convert long recorded speech to text
        '''
        sound = AudioSegment.from_wav(self.path)  
        # split audio sound where silence is 500 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            min_silence_len = 500,
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=1000,
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
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text
        return whole_text

if __name__ == '__main__':
    speach = SpeechtoText()
    speach.large_audio_speech()