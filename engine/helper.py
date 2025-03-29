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
