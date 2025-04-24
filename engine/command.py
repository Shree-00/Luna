import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.helper import clean_speech_text
from engine.vision import describe_surroundings

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 174)

def speak(text):
    text = clean_speech_text(str(text))
    #text = str(text)
    # engine = pyttsx3.init('sapi5')
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id)
    # engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    import speech_recognition as sr
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    try:
        print('Recognizing')
        eel.DisplayMessage('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        # New branch: check if the command is to describe surrounding.
        lowered_query = query.lower()
        vision_commands = [
            "what do you see",
            "describe surrounding",
            "what do you see around",
            "describe the view",
            "what can you see",
            "what's in front of you",
        ]
        if "search" in lowered_query:
            from engine.features import search_in_browser
            search_in_browser(query)

        elif any(kw in lowered_query for kw in vision_commands):
            try:
                print("[Vision] Analyzing surroundings...")
                result = describe_surroundings()
                print(f"[Vision Result] {result}")
                speak(result)
            except Exception as e:
                print(f"[ERROR] Vision command failed: {e}")
                speak("Sorry, I had trouble analyzing the surroundings.")

        elif "open" in lowered_query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in lowered_query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "weather" in lowered_query or "what's the weather" in lowered_query or "how is the weather" in lowered_query:
            from engine.features import getWeather
            getWeather()  
        elif "news" in lowered_query or "headlines" in lowered_query or "today's news" in lowered_query:
            from engine.features import getNews
            speak("Fetching top news headlines.")
            news_list = getNews()
            for i, news in enumerate(news_list, 1):
                speak(f"News {i}: {news}")

        elif any(keyword in lowered_query for keyword in [
            "summarize", "explain", "debug", "analyze", "how to", "optimize", 
            "implement", "code", "rephrase", "describe", "ppt"
        ]):
            from engine.copilot import handle_copilot
            handle_copilot(query)
            print("[Command] Copilot trigger: ", query)

        elif "send message" in lowered_query or "phone call" in lowered_query or "video call" in lowered_query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode do you want to use? WhatsApp or mobile?")
                preference = takecommand()
                print(preference)
                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("What message would you like to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preference:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message do you want to send?")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        print(error_msg)
        speak("An error occurred during processing.")
    
    eel.ShowHood()


#@eel.expose
# def allCommands(message=1):
#     if message == 1:
#         query = takecommand()
#         print(query)
#         eel.senderText(query)
#     else:
#         query = message
#         eel.senderText(query)

#     try:
#         if "open" in query:
#             from engine.features import openCommand
#             openCommand(query)

#         elif "on youtube" in query:
#             from engine.features import PlayYoutube
#             PlayYoutube(query)

#         elif "weather" in query or "what's the weather" in query or "how is the weather" in query:
#             from engine.features import getWeather
#             getWeather()  

#         elif "news" in query or "headlines" in query or "today's news" in query:
#             from engine.features import getNews
#             speak("Fetching top news headlines.")
#             news_list = getNews()
#             for i, news in enumerate(news_list, 1):
#                 speak(f"News {i}: {news}")

#         elif any(keyword in query.lower() for keyword in [
#             "summarize", "explain", "debug", "analyze", 
#             "how to", "optimize", "implement", "code"
#         ]):
#             from engine.copilot import handle_copilot
#             handle_copilot(query)

#         elif "send message" in query or "phone call" in query or "video call" in query:
#             from engine.features import findContact, whatsApp, makeCall, sendMessage
#             contact_no, name = findContact(query)
#             if(contact_no != 0):
#                 speak("Which mode you want to use whatsapp or mobile")
#                 preferance = takecommand()
#                 print(preferance)

#                 if "mobile" in preferance:
#                     if "send message" in query or "send sms" in query: 
#                         speak("what message to send")
#                         message = takecommand()
#                         sendMessage(message, contact_no, name)
#                     elif "phone call" in query:
#                         makeCall(name, contact_no)
#                     else:
#                         speak("please try again")
#                 elif "whatsapp" in preferance:
#                     message = ""
#                     if "send message" in query:
#                         message = 'message'
#                         speak("what message to send")
#                         query = takecommand()
                                        
#                     elif "phone call" in query:
#                         message = 'call'
#                     else:
#                         message = 'video call'
                                        
#                     whatsApp(contact_no, query, message, name)
#         else:
#             from engine.features import chatBot
#             chatBot(query)
#     except Exception as e:
#         error_msg = f"Error occurred: {str(e)}"
#         print(error_msg)
#         speak("An error occurred during processing")
#         # from engine.features import chatBot
#         # chatBot(query)
#         #print("Error occurred:")

#     eel.ShowHood()