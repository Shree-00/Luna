import base64
from io import BytesIO
import pyautogui
import pytesseract
import requests
from engine.helper import clean_speech_text, get_active_window, system_command
from engine.command import speak
from PIL import ImageGrab

# Set your Tesseract path correctly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class AICopilot:
    def __init__(self):
        self.api_key = "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"  # Replace this securely
        self.last_capture = None

    def capture_context(self):
        try:
            window = pyautogui.getActiveWindow()
            if window and window.width > 100:
                bbox = (window.left + 20, window.top + 20, window.right - 20, window.bottom - 20)
                return ImageGrab.grab(bbox)
        except Exception as e:
            print(f"[Copilot] Screen capture error: {e}")
        return ImageGrab.grab()

    def analyze_content(self, prompt):
        screenshot = self.capture_context()
        self.last_capture = screenshot

        try:
            text_content = pytesseract.image_to_string(screenshot)
            if len(text_content.strip()) < 20:
                text_content = "No significant text detected."
        except Exception as e:
            text_content = f"Error reading text: {str(e)}"

        full_prompt = (
            f"Screen context from: {get_active_window()}:\n\n"
            f"{text_content[:2500]}\n\n"
            f"User asked: {prompt}\n\n"
            "Please provide a helpful and detailed assistant response."
        )

        return self.analyze_with_ai(full_prompt, screenshot)

    def analyze_with_ai(self, prompt, image=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]

        if image:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            messages[1]["content"] += f"\n(Base64 image snippet: {img_base64[:100]}...)"

        try:

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "max_tokens": 1000
                }
            )
            data = response.json()
            if 'choices' in data:
                result = data['choices'][0]['message']['content']
                print("[Copilot] AI Response:", result)
                return result
            else:
                print("[Copilot] Full error response:", data)
                return f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"
        except Exception as e:
            return f"Exception while parsing response: {str(e)}"

def handle_copilot(query):
    copilot = AICopilot()
    lowered = query.lower()

    if any(k in lowered for k in ["summarize", "text", "document"]):
        prompt = "Summarize the following content: " + query
    elif "find error" in lowered or "debug" in lowered:
        prompt = "Analyze and find issues in the code: " + query
    elif any(k in lowered for k in ["help me code", "explain", "rephrase"]):
        prompt = "Please assist with this request: " + query
    elif "describe" in lowered or "detailed description" in lowered:
        prompt = "Provide a detailed description of what's visible: " + query
    elif "ppt" in lowered or "make ppt" in lowered:
        prompt = "Generate a PowerPoint presentation based on: " + query
    else:
        prompt = query

    response = copilot.analyze_content(prompt)
    speak(response if response else "I couldn't generate a response.")

# import base64
# from io import BytesIO
# import pyautogui
# import pytesseract
# from engine.helper import clean_speech_text, get_active_window, system_command
# from engine.command import speak
# from PIL import ImageGrab
# from transformers import LlamaForCausalLM, LlamaTokenizer
# import torch

# # Set your Tesseract path correctly
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# class AICopilot:
#     def __init__(self):
#         # Load LLaMA model and tokenizer
#         self.tokenizer = LlamaTokenizer.from_pretrained("huggingface/llama-7b")  # Use the desired LLaMA variant (small, medium, large)
#         self.model = LlamaForCausalLM.from_pretrained("huggingface/llama-7b")  # Load the LLaMA model (use a smaller model if necessary)

#         self.last_capture = None

#     def capture_context(self):
#         try:
#             window = pyautogui.getActiveWindow()
#             if window and window.width > 100:
#                 bbox = (window.left + 20, window.top + 20, window.right - 20, window.bottom - 20)
#                 return ImageGrab.grab(bbox)
#         except Exception as e:
#             print(f"[Copilot] Screen capture error: {e}")
#         return ImageGrab.grab()

#     def analyze_content(self, prompt):
#         screenshot = self.capture_context()
#         self.last_capture = screenshot

#         try:
#             text_content = pytesseract.image_to_string(screenshot)
#             if len(text_content.strip()) < 20:
#                 text_content = "No significant text detected."
#         except Exception as e:
#             text_content = f"Error reading text: {str(e)}"

#         full_prompt = (
#             f"Screen context from: {get_active_window()}:\n\n"
#             f"{text_content[:2500]}\n\n"
#             f"User asked: {prompt}\n\n"
#             "Please provide a helpful and detailed assistant response."
#         )

#         return self.analyze_with_ai(full_prompt)

#     def analyze_with_ai(self, prompt):
#         # Tokenize the input prompt
#         inputs = self.tokenizer(prompt, return_tensors="pt")

#         # Generate a response using LLaMA
#         outputs = self.model.generate(inputs["input_ids"], max_length=150, num_return_sequences=1, pad_token_id=self.tokenizer.eos_token_id)

#         # Decode and return the response
#         result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return result

# def handle_copilot(query):
#     copilot = AICopilot()
#     lowered = query.lower()

#     if any(k in lowered for k in ["summarize", "text", "document"]):
#         prompt = "Summarize the following content: " + query
#     elif "find error" in lowered or "debug" in lowered:
#         prompt = "Analyze and find issues in the code: " + query
#     elif any(k in lowered for k in ["help me code", "explain", "rephrase"]):
#         prompt = "Please assist with this request: " + query
#     elif "describe" in lowered or "detailed description" in lowered:
#         prompt = "Provide a detailed description of what's visible: " + query
#     elif "ppt" in lowered or "make ppt" in lowered:
#         prompt = "Generate a PowerPoint presentation based on: " + query
#     else:
#         prompt = query

#     response = copilot.analyze_content(prompt)
#     speak(response if response else "I couldn't generate a response.")

