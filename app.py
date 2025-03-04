import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
import os
import uuid
import pyttsx3
from io import BytesIO
from PIL import Image
import base64

# Initialize Text-to-Speech Engine (Only for local execution)
def speak(text):
    if "STREAMLIT_SERVER" not in os.environ:  # Only run locally
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# Streamlit Page Config
st.set_page_config(page_title="QR Code Generator", page_icon="📷", layout="wide")

# Function to Play Audio using Base64 Encoding
def play_audio(file_path):
    """Plays an audio file using base64 encoding to avoid Streamlit media file errors."""
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# Play welcome audio when the app opens
play_audio("welcome.mp3")

# Custom CSS for a 3D Attractive UI with Enhanced Animations
st.markdown("""
    <style>
        body { background-color: #1E1E1E; color: white; text-align: center; }
        .stTextInput, .stTextArea, .stButton > button { 
            border-radius: 12px; 
            padding: 12px; 
            border: 2px solid #FF8A00; 
            font-size: 16px;
            box-shadow: 3px 3px 10px rgba(255, 138, 0, 0.5);
            transition: all 0.3s ease-in-out;
        }
        .stButton > button { 
            background: linear-gradient(145deg, #ff8a00, #da1b60); 
            color: white; font-weight: bold; 
            transition: all 0.3s ease-in-out;
            box-shadow: 4px 4px 15px rgba(255, 138, 0, 0.7);
        }
        .stButton > button:hover { 
            transform: scale(1.1); 
            box-shadow: 6px 6px 20px rgba(255, 138, 0, 0.9);
        }
        .qr-container { 
            display: flex; justify-content: center; align-items: center; 
            flex-direction: column; padding: 20px; 
        }
        .stColorPicker { margin: 10px 0; }
        .title-text { 
            color: #FF8A00; font-size: 35px; font-weight: bold; 
            text-shadow: 2px 2px 10px rgba(255, 138, 0, 0.8);
            animation: glow 1.5s infinite alternate;
        }
        @keyframes glow {
            0% { text-shadow: 2px 2px 10px rgba(255, 138, 0, 0.8); }
            100% { text-shadow: 4px 4px 20px rgba(255, 138, 0, 1); }
        }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown("""
    <h1 class='title-text'>📷 3D QR Code Generator</h1>
    <p style='text-align: center; color: white; font-size: 18px;'>
        Generate stunning QR codes instantly for URLs, texts, or any data in a modern 3D-styled UI!
    </p>
    <p style='text-align: center; color: #DA1B60; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 5px rgba(218, 27, 96, 0.8);'>
        Made by Jareer Shafiq
    </p>
""", unsafe_allow_html=True)

# User Input
text_input = st.text_input("🔤 Enter text or URL to generate QR Code:")
color_fg = st.color_picker("🎨 Pick QR Code Foreground Color", "#FF8A00")
color_bg = st.color_picker("🎨 Pick QR Code Background Color", "#FFFFFF")
add_logo = st.checkbox("📌 Add Logo to QR Code")

# Public URL for Deployment (Change this to your deployed app URL)
APP_URL = "https://your-app-name.streamlit.app"

# Store QR Code History
if "qr_history" not in st.session_state:
    st.session_state.qr_history = []

# Generate QR Code Function
def generate_qr(data, fg_color, bg_color, logo=False):
    qr = qrcode.QRCode(
        version=1, box_size=10, border=5
    )
    full_url = f"{APP_URL}?data={data}"
    qr.add_data(full_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    
    if logo and os.path.exists("logo.png"):
        logo_img = Image.open("logo.png").convert("RGBA")
        img = img.convert("RGBA")
        img_w, img_h = img.size
        logo_size = img_w // 4
        logo_img = logo_img.resize((logo_size, logo_size))
        pos = ((img_w - logo_size) // 2, (img_h - logo_size) // 2)
        img.paste(logo_img, pos, logo_img)
    elif logo:
        st.warning("⚠️ Logo file not found! Please add 'logo.png' to the project directory.")
    
    return img

if st.button("🚀 Generate QR Code"):
    if text_input:
        unique_filename = f"qrcode_{uuid.uuid4().hex}.png"
        img = generate_qr(text_input, color_fg, color_bg, add_logo)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf, caption="🎨 Your 3D QR Code", use_container_width=True)
        
        # Store QR Code Entry
        st.session_state.qr_history.append(text_input)
        
        # Download Button
        st.download_button(
            label="📥 Download QR Code",
            data=buf.getvalue(),
            file_name=unique_filename,
            mime="image/png",
            help="Click to download your QR Code"
        )
    else:
        st.warning("⚠️ Please enter some text or a URL!")

# Display QR Code History
if st.session_state.qr_history:
    st.subheader("📜 QR Code History")
    df = pd.DataFrame({"Scanned Data": st.session_state.qr_history})
    fig = px.bar(df, x="Scanned Data", title="📊 QR Code History", color_discrete_sequence=["#FF8A00"])
    st.plotly_chart(fig)
