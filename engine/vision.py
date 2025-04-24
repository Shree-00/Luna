import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from ultralytics import YOLO
from hugchat import hugchat

# Load local BLIP model
BLIP_MODEL_PATH = "engine/model/blip"
blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_PATH, use_fast=False)
blip_model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_PATH)

# Load local YOLOv8 model
YOLO_MODEL_PATH = "engine/model/yolo/yolov8n.pt"
yolo_model = YOLO(YOLO_MODEL_PATH)
class_names = yolo_model.model.names

def get_position(x, width):
    """Get horizontal position."""
    if x < width / 3:
        return "left"
    elif x < 2 * width / 3:
        return "center"
    return "right"

def generate_caption_with_blip(frame):
    """Generate image caption using BLIP."""
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = blip_processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    return blip_processor.decode(out[0], skip_special_tokens=True)

def generate_natural_response(prompt):
    """Generate descriptive sentence using HugChat."""
    cookies_path = Path(__file__).parent / "cookies.json"
    chatbot = hugchat.ChatBot(cookie_path=str(cookies_path))
    response = chatbot.chat(prompt)
    return str(response).strip()

def describe_surroundings():
    """Detect objects and return a natural-language description."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Sorry, I couldn't access the camera."

    height, width, _ = frame.shape
    results = yolo_model.predict(source=frame, conf=0.5, verbose=False)

    if not results or len(results[0].boxes) == 0:
        # No objects detected — fallback to image caption
        caption = generate_caption_with_blip(frame)
        prompt = f"The image caption is: '{caption}'. Describe this scene naturally like a helpful assistant."
        try:
            response = generate_natural_response(prompt)
            return response
        except Exception as e:
            print("[ERROR HugChat - fallback to caption only]", e)
            return caption

    # Objects detected — add directional context
    descriptions = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0].item())
        label = class_names[cls_id]
        x_center = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
        position = get_position(x_center, width)
        descriptions.append(f"a {label} on the {position}")

    summary = ", ".join(descriptions)
    caption = generate_caption_with_blip(frame)
    prompt = (
        f"There are {summary}. Also, an image caption reads: '{caption}'. "
        f"Based on this, describe the scene naturally like a human assistant would. Don't make up anything."
    )

    try:
        response = generate_natural_response(prompt)
        return response
    except Exception as e:
        print("[ERROR HugChat - fallback to object summary]", e)
        return summary


# import cv2
# import numpy as np
# from pathlib import Path
# from collections import defaultdict
# from hugchat import hugchat

# # Paths to YOLO files
# YOLO_DIR = Path(__file__).parent / "model" / "yolo"
# CONFIG_PATH = str(YOLO_DIR / "yolov3.cfg")
# WEIGHTS_PATH = str(YOLO_DIR / "yolov3.weights")
# NAMES_PATH = str(YOLO_DIR / "coco.names")

# # Load class names
# with open(NAMES_PATH, "r") as f:
#     class_names = [line.strip() for line in f.readlines()]

# # Load YOLOv3 network
# net = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# def get_position(x, width):
#     """Divide the frame horizontally into left, center, and right."""
#     if x < width * 1/3:
#         return "left"
#     elif x < width * 2/3:
#         return "center"
#     else:
#         return "right"

# def generate_natural_response(prompt):
#     """
#     Generate a human-like response from HugChat.
#     """
#     cookies_path = Path(__file__).parent / "cookies.json"
#     chatbot = hugchat.ChatBot(cookie_path=str(cookies_path))
#     response = chatbot.chat(prompt)

#     try:
#         if isinstance(response, dict) and "choices" in response:
#             return response["choices"][0]["text"].strip()
#         return str(response).strip()
#     except Exception as e:
#         print(f"[ERROR] Processing HugChat response failed: {e}")
#         raise Exception("HugChat response format error.")

# def describe_surroundings():
#     """
#     Capture a frame, detect objects using YOLOv3, and describe them with HugChat.
#     """
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if not ret:
#         return "Sorry, I couldn't access the camera."

#     height, width, _ = frame.shape
#     blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)

#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
#     outputs = net.forward(output_layers)

#     boxes = []
#     confidences = []
#     class_ids = []

#     for output in outputs:
#         for detection in output:
#             scores = detection[5:]
#             class_id = int(np.argmax(scores))
#             confidence = scores[class_id]
#             if confidence > 0.6:
#                 center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
#                 x = int(center_x - w / 2)
#                 y = int(center_y - h / 2)
#                 boxes.append([x, y, int(w), int(h)])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)

#     indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.6)

#     if len(indices) == 0:
#         return "I don't see anything noteworthy right now."

#     descriptions = []
#     for i in indices.flatten():
#         x, y, w, h = boxes[i]
#         label = class_names[class_ids[i]]
#         position = get_position(x + w // 2, width)
#         descriptions.append(f"a {label} on the {position}")

#     summary = ", ".join(descriptions)
#     prompt = (
#     f"There are {summary}. "
#     "Based on this list of objects and positions, describe the scene realistically "
#     "without making up details."
# )


#     try:
#         return generate_natural_response(prompt)
#     except Exception as e:
#         print(f"[ERROR] HugChat failed: {e}")
#         return f"I see {summary}."
