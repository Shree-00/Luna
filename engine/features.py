import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from hugchat import hugchat
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui as autogui 
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import openai
from engine.helper import extract_yt_term, remove_words
import torch
from pyowm.utils import config
from pyowm.utils import timestamps
import requests
from transformers import pipeline
import shutil
#from engine.vision import describe_surroundings


conn = sqlite3.connect("Luna.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# def openCommand(query):
#     query = query.replace(ASSISTANT_NAME, "")
#     query = query.replace("open", "")
#     query = query.strip()
    
#     app_name = query  # app_name remains in the same case for human output

#     if app_name != "":
#         try:
#             # Look in system commands (for locally installed apps)
#             cursor.execute('SELECT path FROM sys_command WHERE lower(name)=?', (app_name.lower(),))
#             results = cursor.fetchall()

#             if len(results) != 0:
#                 speak("Opening " + app_name)
#                 os.startfile(results[0][0])
#                 return  # Exit once successfully launched

#             # Next, check web commands (for web app URLs)
#             cursor.execute('SELECT path FROM web_command WHERE lower(name)=?', (app_name.lower(),))
#             results = cursor.fetchall()
            
#             if len(results) != 0:
#                 speak("Opening " + app_name)
#                 import webbrowser
#                 webbrowser.open(results[0][0])
#                 return

#             # If none of the above, try executing as a system command
#             speak(" okay, Opening " + app_name)
#             try:
#                 os.system('start ' + app_name)
#             except Exception:
#                 speak("Not found, please make sure you typed the name correctly.")
#         except Exception as e:
#             speak("Something went wrong: " + str(e))

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip()

    app_name = query.lower()

    if app_name != "":
        try:
            # 1. Known Windows app full paths (like PowerPoint, Word, etc.)
            known_apps = {
                "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "vs code": r"C:\Users\shreeya\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "visual studio code": r"C:\Users\shreeya\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "command prompt": "C:\WINDOWS\system32\cmd.exe",
                "android studio": "C:\Program Files\Android\Android Studio\bin\studio64.exe"
            }

            for key in known_apps:
                if key in app_name:
                    exe_path = os.path.expandvars(known_apps[key])
                    speak(f"Opening {key}")
                    os.startfile(exe_path)
                    return

            # 2. Try finding via system PATH using `where`
            result = subprocess.run(["where", app_name], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]
                speak(f"Opening {app_name}")
                os.startfile(path)
                return

            # 3. Open common web apps
            web_apps = {
                "youtube": "https://www.youtube.com",
                "gmail": "https://mail.google.com",
                "google": "https://www.google.com",
                "chatgpt": "https://chat.openai.com",
                "whatsapp": "https://web.whatsapp.com",
                "facebook": "https://www.facebook.com",
                "instagram": "https://www.instagram.com",
                "github": "https://github.com/",
                "spotify": "https://open.spotify.com/",
                "classroom": "https://classroom.google.com/"
            }

            if app_name in web_apps:
                speak(f"Opening {app_name}")
                webbrowser.open(web_apps[app_name])
                return

            # 4. Final fallback: try system execution (may still fail)
            speak(f"Trying to open {app_name}")
            os.system(f'start {app_name}')
        except Exception as e:
            speak(f"Something went wrong: {str(e)}")
    else:
        speak("Please specify an app to open.")

def search_in_browser(query):
    # Remove the keyword 'search' from the query
    search_term = query.lower().replace("search", "").strip()
    if search_term == "":
        speak("I did not get any search terms. Please say the search term after the word search.")
        return
    search_url = "https://www.google.com/search?q=" + search_term.replace(" ", "+")
    speak("Searching for " + search_term)
    import webbrowser
    webbrowser.open(search_url)

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("playing "+search_term+ " on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    # Your credentials and wake word path
    access_key = "Ii5PDp9K4op3ipw5/6/l6B9EEcvFmKa2ndQ+dEfHQ1KYrstdRXTukA==" 
    keyword_path = r"D:\project\dist\Hi-Luna_en_windows_v3_0_0.ppn"

    try:
        # Initialize with CUSTOM wake word (changed from keywords to keyword_paths)
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path]  # Use your .ppn file
        ) 
        
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        #print("Listening for 'Hi Luna'...")
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detected")
                # Win+J shortcut
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Cleanup resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 20
        luna_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 14
        message = ''
        luna_message = "calling to "+name

    else:
        target_tab = 13
        message = ''
        luna_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(luna_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

from datetime import datetime

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! How can I assist you today?"
    elif 12 <= hour < 17:
        return "Good afternoon! What can I do for you?"
    elif 17 <= hour < 23:
        return "Good evening! How may I help you?"
    else:
        return "What's up night owl! ?"
    
from pyowm import OWM
from engine.config import OWM_API_KEY
import geocoder

def getWeather(city=None):
    try:
        owm = OWM(OWM_API_KEY)
        mgr = owm.weather_manager()
        
        if not city:
            # Attempt to auto-detect your current city by IP
            g = geocoder.ip('me')
            if g.ok and g.city:
                city = g.city
            else:
                city = "New York"  # Fallback city if auto-detection fails

        observation = mgr.weather_at_place(city)
        w = observation.weather

        # Construct a weather report
        weather_str = f"In {city}: {w.detailed_status.capitalize()}, Temp: {w.temperature('celsius')['temp']}°C"
        speak(weather_str)
    except Exception as e:
        speak(f"Unable to get weather information: {str(e)}")


def getNews():
    API_KEY = "d4a7f2ba04964f22a3b49a4074bc5238"  # replace with your actual key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey=d4a7f2ba04964f22a3b49a4074bc5238"

    response = requests.get(url)
    data = response.json()

    news_list = []

    if data["status"] == "ok" and data["totalResults"] > 0:
        for article in data["articles"][:5]:  # Limit to top 5
            news_list.append(article["title"])
    else:
        news_list.append("Sorry, I couldn't fetch the news right now.")

    return news_list

