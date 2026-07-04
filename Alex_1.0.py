'''
pip install SpeechRecognition #done
pip install pyttsx3 
pip install pyautogui
pip install pyaudio
pip install -U openai-whisper #!!!!!!!!done
pip install torch
pip install sounddevice
pip install numpy
pip install openai
'''

#VOLUME UP AND DOWN, WILL BE SOON!!!!!!
import urllib;import time 
import speech_recognition as sr
import pyttsx3# dont need this. but still , let it be there 
import webbrowser
import os
import time
import subprocess
import tkinter as tk
from threading import Thread
from queue import  Queue  #for the bugs we r going to use Queue instead of pyttsx3



#setup
listener = sr.Recognizer()
listener.energy_threshold = 150
listener.dynamic_energy_threshold = True
listener.pause_threshold = 1.0
listener.phrase_threshold = 0.3



#speech queue
speech_queue=Queue()
#voice explicity
 
engine = pyttsx3.init()
engine.setProperty("rate", 170)

voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)


mic_index = 1 #mic index



#speak function
def speak(text):
    gui_update_status(f"Alex: {text}")
    speech_queue.put(text)
#listen 
def listen():
    with sr.Microphone(device_index=mic_index) as source:#opens and closes the mic...
        listener.adjust_for_ambient_noise(source, duration=0.5)
        gui_update_status("Listening...")
        audio = listener.listen(source)

    try:
        text = listener.recognize_google(audio, language="en-US")
        gui_update_status(f"Heard: {text}")
        return text.lower()
    except sr.UnknownValueError:
        gui_update_status("Heard but couldn’t understand")
        return ""
    except sr.RequestError as e:
        gui_update_status(f"API error: {e}")
        return ""

#speech_worker
def speech_worker():
    while True:
        text = speech_queue.get()
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

#gui
def gui_update_status(text):
    status_label.config(text=text)

def run_assistant():
    speak("Alex is online")

    while True:
        wake = listen()
        if "hey alex" in wake:
            speak("Yes, listening")
            
            time.sleep(0.5)
            command = listen()

        # COMMANDS
            #GOOGLE
            if "open google" in command:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
            #YOUTUBE
            elif "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            #NOTEPAD
            elif "open notepad" in command:
                speak("Opening Notepad")
                os.system("notepad")
            #EXPLORER DOWNLOADS
            elif "open downloads" in command:
                speak("Opening Downloads folder")
                os.startfile(os.path.join(os.environ["USERPROFILE"], "Downloads"))
            #VOLUME UP
            elif "increase volume" in command or "volume up" in command:

                speak("Turning volume up")
                subprocess.call("nircmd.exe changesysvolume 5000", shell=True)
            #VOLUME DOWN
            elif "decrease volume" in  command or "volume down" in command:
                speak("Turning volume down")
                subprocess.call("nircmd.exe changesysvolume -5000", shell=True)

            elif "shut down" in command or "shutdown" in command:
                speak("Say confirm shutdown to proceed")
                confirm = listen()
                if "confirm shutdown" in confirm or "confirm shut down" in confirm:
                    speak("Shutting down")
                    os.system("shutdown /s /t 5")
                else:
                    speak("Shutdown cancelled")

            elif "stop" in command or "exit"in command  or "close" in command:
                speak("Good bye....")
                root.quit()
                break

            else:
                speak("I did not understand that command")

#TKINTER GUI
root = tk.Tk()
root.title("Alex Assistant")
root.geometry("450x200")
root.configure(bg="pink")
root.resizable(False, False)
tk.Button(root, text="Close", command=root.quit, bg="skyblue", fg="white", font=("Sogoe UI", 12)).pack(pady=10)

status_label = tk.Label(root, text="Initializing...", font=("Helvetica", 14), wraplength=400,bg="pink")
status_label.pack(pady=60)


#Start assistant in separate thread so GUI doesnt freeze
Thread(target=run_assistant, daemon=True).start()
Thread(target=speech_worker,daemon=True).start()
root.mainloop()






