import speech_recognition as sr
from textblob import TextBlob

class VoiceToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def recognize_speech(self, audio_path=None):
        """
        Recognize speech from microphone or audio file
        Returns: recognized text or None if failed
        """
        try:
            if audio_path is None:
                # Record from microphone
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, timeout=10)
            else:
                # Load from audio file
                with sr.AudioFile(audio_path) as source:
                    audio = self.recognizer.record(source)
            
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text.lower().strip()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def text_to_signs(self, text):
        """
        Convert text to individual signs/letters
        Returns: list of characters
        """
        # Remove spaces and convert to lowercase
        text = text.lower().replace(" ", "")
        return list(text)
    
    def correct_text(self, text):
        """
        Correct text spelling using TextBlob
        """
        try:
            blob = TextBlob(text)
            return str(blob.correct())
        except:
            return text
