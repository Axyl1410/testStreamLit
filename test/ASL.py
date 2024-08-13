import os
from PIL import Image
import streamlit as st
import time

# Function to display sign language images
def display_images(text):
    img_dir = "D:/test1/NCKH4/test/images/ASL"
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
