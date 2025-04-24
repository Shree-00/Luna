import re


def extract_yt_term(command):
    #define regular expressionpattern to capture the search song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to find the match in command
    match = re.search(pattern, command, re.IGNORECASE)
    #if a match is found, return the extract song name, otherwise return none
    return match.group(1) if match else None

# Helper Function to remove unwanted words from query

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

#Example usage
# input_string = "make a phone call to mumma"
# words_to_remove = ['make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', '']

# result = remove_words(input_string, words_to_remove)
# print(result)

# engine/helper.py
import re

def clean_speech_text(text):
    """Clean text for speech output"""
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?\'\-]', ' ', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove markdown formatting
    text = re.sub(r'\*{1,3}', '', text)
    # Convert hashtags to normal text
    text = re.sub(r'#(\w+)', r'\1', text)
    # # Remove code blocks
    # text = re.sub(r'```.*?```', 'code example', text, flags=re.DOTALL)
    # # # Remove URLs
    # text = re.sub(r'http\S+', 'link', text)
    return text.strip()

import pyautogui

def get_active_window():
    """Get current active window title"""
    try:
        window = pyautogui.getActiveWindow()
        return window.title if window else "Unknown Application"
    except Exception as e:
        print(f"Window detection error: {e}")
        return "Desktop"

def get_clipboard():
    import pyperclip
    return pyperclip.paste()

def system_command(cmd):
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def validate_text_content(text):
    checks = [
        (r'\b[a-z]{3,}\b', "No meaningful words detected"),
        (r'[.!?]', "No sentence structure found"),
        (r'\d', "No numerical data present")
    ]
    
    for pattern, message in checks:
        if not re.search(pattern, text):
            return False, message
    return True, "Valid text"