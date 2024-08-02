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


# define function to display sign language images
def display_images(text):
    # get the file path of the images directory
    img_dir = "images/ASL"

    # initialize variable to track image position
    image_pos = st.empty()

    # iterate through the text and display sign language images
    for char in text:
        if char.isalpha():
            # display sign language image for the alphabet
            img_path = os.path.join(img_dir, f"{char}_test.jpg")
            img = Image.open(img_path)

            # update the position of the image
            image_pos.image(img, width=500)

            # wait for 2 seconds before displaying the next image
            time.sleep(2)

            # remove the image
            image_pos.empty()
        elif char == ' ':
            # display space image for space character
            img_path = os.path.join(img_dir, "nothing_test.jpg")
            img = Image.open(img_path)

            # update the position of the image
            image_pos.image(img, width=500)

            # wait for 2 seconds before displaying the next image
            time.sleep(2)

            # remove the image
            image_pos.empty()

    # wait for 2 seconds before removing the last image
    time.sleep(2)
    image_pos.empty()


# Initialize the TTS synthesizer
synthesizer = initialize_tts()

text = st.text_input("Enter text:")
# convert text to lowercase
text = text.lower()

# Perform TTS
text_to_speech(synthesizer, text)

# display sign language images
display_images(text)
