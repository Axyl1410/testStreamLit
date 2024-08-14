import os
from PIL import Image
import streamlit as st
import time
import azure.cognitiveservices.speech as speechsdk


# Function to initialize TTS
def initialize_tts():
    speech_key = "47d4aeb39aed4cc0b0143a5359d9af56"
    service_region = "eastasia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    return speechsdk.SpeechSynthesizer(speech_config=speech_config)


# Function to perform TTS
def text_to_speech(synthesizer, text):
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))


# Function to display sign language images
def display_images(text):
    img_dir = "/images/ASL"
    image_pos = st.empty()

    for char in text:
        if char.isalpha():
            img_path = os.path.join(img_dir, f"{char}_test.jpg")
            img = Image.open(img_path)
            image_pos.image(img, width=500)
            time.sleep(2)
            image_pos.empty()
        elif char == ' ':
            img_path = os.path.join(img_dir, "nothing_test.jpg")
            img = Image.open(img_path)
            image_pos.image(img, width=500)
            time.sleep(2)
            image_pos.empty()

    time.sleep(2)
    image_pos.empty()

# Get user input and display sign language images
text = st.text_input("Enter text:")
text = text.lower()
display_images(text)
