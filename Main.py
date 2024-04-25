import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_key = os.getenv("OPENAI_KEY")


#Set up OpenAI and speech modules
import openai
openai.api_key = OPENAI_key
r = sr.Recognizer()


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def record_text():
   try:
       with sr.Microphone() as source:
           r.adjust_for_ambient_noise(source, duration=0.2)
           print("I am listening...")
           audio = r.listen(source)
           text = r.recognize_google(audio) #listens for audio and stores it in variable
           print(f"Recognized text: {text}") #printing recognized audio
           return text
   except sr.RequestError as e:
           print(f"Could not request results: {e}")
   except sr.UnknownValueError:
           print("Could not understand audio")
   except Exception as e:
           print(f"An error occured: {e}")
   return None

# Function that sends message to ChatGPT and return a response
def send_to_chatGPT(text):
    try:
        if len(text) > 10:
            text = text[-10:]
        response = openai.ChatCompletion.create(
            model='gpt3.5-turbo',
            messages = text,
            max_tokens = 1500
        )
        content = response['choices'][0]['message']['content']
        text.append({"role" : "system","content" : content})
        return content
    except Exception as e:
        print(f"Failed to send message to ChatGPT: {e}")
        return "Error connecting to AI"


messages = [{"role" : "system", "content" : "My name is Jarvis. How can I help you?"}]
SpeakText(messages[-1]["content"])

while True:
    try:
        text = record_text()
        if text is None or text.lower() == 'exit':
            print("Exiting")
            break
        if text:
            messages.append({"role" : "system","content" : text})
            responce = send_to_chatGPT(messages)
            SpeakText(responce)
        else:
            SpeakText("Please say that again")
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...")
        break

