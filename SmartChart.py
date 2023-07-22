import streamlit as st
from datetime import date
from streamlit_option_menu import option_menu
from ptcare import patientStates
from ptcare import contras
from ptcare import warnings
from treatments import treatmentDescription
import streamlit as st
import openai
import whisper
from audio_recorder_streamlit import audio_recorder
import time
import glob
import os
from gtts import gTTS
from googletrans import Translator
from locationServices import get_location
from locationServices import get_location
from locationServices import getLocationType
from locationServices import getRecDest
from locationServices import rearrange_places
from locationServices import get_weather
from vital_entry import analyze_vitals
import streamlit as st
import cv2
import os
import platform
from pharmacology import drugDescription
import requests
import streamlit as st
from google.cloud import vision
from PIL import Image
import io
from google.oauth2 import service_account
from streamlit_js_eval import streamlit_js_eval
from urllib.parse import quote
import tensorflow as tf
from keras.models import load_model
import numpy as np
from PIL import Image, ImageOps  # Install pillow instead of PIL
import streamlit.components.v1 as components
import random
import traceback

st.set_page_config(
    page_title='SmartChart',
    page_icon='ambulance'
)   

def set_pulse_rate_prefix():
    st.session_state.input_state["pulse_rate"] = st.session_state.pulse_rate 
    if st.session_state.pulse_rate!="" and not (60 <= int(st.session_state.pulse_rate) <= 140):
        st.session_state[f"pulse_rate_prefix"] = "⚠️ "
    else:
        st.session_state[f"pulse_rate_prefix"] = ""

def set_blood_pressure_prefix():
    st.session_state.input_state["blood_pressure"] = st.session_state.blood_pressure 
    if st.session_state.blood_pressure!="" and not (60 <= int(st.session_state.blood_pressure) <= 90):
        st.session_state[f"blood_pressure_prefix"] = "⚠️ "
    else:
        st.session_state[f"blood_pressure_prefix"] = ""

def set_temperature_prefix():
    st.session_state.input_state["temperature"] = st.session_state.temperature 
    if st.session_state.temperature!="" and not (95 <= int(st.session_state.temperature) <= 100.4):
        st.session_state[f"temperature_prefix"] = "⚠️ "
    else:
        st.session_state[f"temperature_prefix"] = ""

def set_pupils_prefix():
    st.session_state.input_state["pupils"] = st.session_state.pupils 
    if st.session_state.pupils!="" and not (st.session_state.pupils.lower() in ["perrl", "normal", "regular", "healthy"]):
        st.session_state[f"pupils_prefix"] = "⚠️ "
    else:
        st.session_state[f"pupils_prefix"] = ""

def set_respiratory_rate_prefix():
    st.session_state.input_state["respiratory_rate"] = st.session_state.respiratory_rate 
    if st.session_state.respiratory_rate!="" and not (12<=int(st.session_state.respiratory_rate)<=25):
        st.session_state[f"respiratory_rate_prefix"] = "⚠️ "
    else:
        st.session_state[f"respiratory_rate_prefix"] = ""

def set_pulse_ox_prefix():
    st.session_state.input_state["pulse_ox"] = st.session_state.pulse_ox
    if st.session_state.pulse_ox!="" and not (int(st.session_state.pulse_ox)>=95):
        st.session_state[f"pulse_ox_prefix"] = "⚠️ "
    else:
        st.session_state[f"pulse_ox_prefix"] = ""

def set_skin_condition_prefix():
    st.session_state.input_state["skin_condition"] = st.session_state.skin_condition 
    if st.session_state.skin_condition!="" and not (st.session_state.skin_condition.lower() in ["normal", "regular", "healthy", "clear"]):
        st.session_state[f"skin_condition_prefix"] = "⚠️ "
    else:
        st.session_state[f"skin_condition_prefix"] = ""

def set_breath_sounds_prefix():
    st.session_state.input_state["breath_sounds"] = st.session_state.breath_sounds 
    if st.session_state.breath_sounds!="" and not (st.session_state.breath_sounds.lower() in ["normal", "regular", "healthy", "clear", "clear bilaterally", "bilaterally clear"]):
        st.session_state[f"breath_sounds_prefix"] = "⚠️ "
    else:
        st.session_state[f"breath_sounds_prefix"] = ""

def set_avpu_prefix():
    st.session_state.input_state["avpu"] = st.session_state.avpu 
    if st.session_state.avpu!="" and not (st.session_state.avpu.lower()  == "alert"):
        st.session_state[f"avpu_prefix"] = "⚠️ "
    else:
        st.session_state[f"avpu_prefix"] = ""

def set_gcs_prefix():
    st.session_state.input_state["gcs"] = st.session_state.gcs 
    if st.session_state.gcs!="" and not (int(st.session_state.gcs) >= 15):
        st.session_state[f"gcs_prefix"] = "⚠️ "
    else:
        st.session_state[f"gcs_prefix"] = ""

##mega try catch block
try:
        
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    model_engine = "text-davinci-003"
    openai.api_key = "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"

    if "input_state" not in st.session_state:
        st.session_state.input_state = {}
        st.session_state.input_state["temperature"] = ""
        st.session_state.input_state["pulse_rate"] = ""
        st.session_state.input_state["pulse_ox"] = ""
        st.session_state.input_state["selected"] = ""
        st.session_state.input_state["scroll_to_top"] = ""
        st.session_state.input_state["screen_width"] = 0
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    def classify(image_path):
        # Load the labels
        class_names = open("labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(image_path).convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = image_model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]

        # Print prediction and confidence score
        return class_name[2:].replace("\n", "")

    def streamlit_menu():
        st.session_state.input_state["screen_width"] = streamlit_js_eval(js_expressions='screen.width', want_output = True, key = 'SCR')
        try:
            if(st.session_state.input_state["screen_width"] > 1000):

                options_list = ["Patient Chart",  "Recommended EMS Actions", "Patient Communication", "Patient Assessment", "Transport Direction"]

                #horizontal menu with custom style
                selected = option_menu(
                    menu_title=None,  # required
                    options=options_list,  # required
                    icons=["house", "book",  "mic", "camera", "map"],  # optional
                    default_index=0,  # optional
                    orientation="horizontal",
                    styles={
                            # "nav-link-selected": {"font-weight": "normal", "background": "linear-gradient(to right, red, orange)"},
                            "nav-link-selected": {"font-weight": "normal", "background": "#0066FF"},
                            "nav-link": {"display": "inline-block", "margin-right": "10px"},
                    "icon": {"display": "block", "margin-bottom": "5px"}
                    }
                )
            else:
                selected = st.selectbox("Navigate", ["Patient Chart",  "Recommended EMS Actions", "Patient Communication", "Patient Assessment", "Transport Direction"])
            if(st.session_state.input_state["selected"] != selected):
                st.session_state.input_state["scroll_to_top"] = True
                components.html(
                    f"""
                        <script>
                            window.parent.document.querySelector('section.main').scrollTo(0, 150);
                        </script>
                    """,
                    height=0
                    )
            st.session_state.input_state["selected"] = selected
            return selected
        except:
            return 0

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("‎")
    with col2:
        st.subheader("‎")


    @st.cache_resource
    def load_image_model():
        return load_model("keras_model.h5", compile=False)

    image_model = load_image_model()


    @st.cache_resource
    def load_model():
        return whisper.load_model("base")

    model = load_model()


    selected = streamlit_menu()

    #home page to take patient vitals
    if selected == "Patient Chart":


        col2, col1 = st.columns([4, 1])
        with col2:
            st.title(f" SmartChart Patient Record")
        with col1:
            st.image("SmartChartLogo.jpg", width=75)

        st.write(f"Collect patient info and receive the correct protocols all in one place.")
        st.session_state['vitals_transcription'] = ''

        def detect_text(path):
            """Detects text in the file."""
            credentials = service_account.Credentials.from_service_account_file('./ServiceAccountToken.json')
            client = vision.ImageAnnotatorClient(credentials=credentials)

            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            response = client.text_detection(image=image)
            texts = response.text_annotations
            return texts[0].description if texts else ""
            

        st.subheader("Charting Tools 🔧")

        if('uploaded_image' not in st.session_state):
            st.session_state['uploaded_image'] = False

        col1, col2 = st.columns(2)
        with col1:
            # Image Uploader
            input_expander = st.expander("Upload Handwritten PCR 📓")

            uploaded_file = input_expander.file_uploader("Choose an image...")
            if uploaded_file is None:
                st.session_state['uploaded_image'] = False
            if uploaded_file is not None and st.session_state['uploaded_image'] == False:
                st.session_state['uploaded_image'] = True
                image = Image.open(uploaded_file)
                # Rotate the image if necessary before transcription
                if st.session_state.input_state["screen_width"] < 1000:
                    image = image.rotate(270, expand=True)
                # Save the potentially rotated image to a temporary file, so it can be read by Google Vision
                image.save("temp.jpg")
                # Use Google Vision to get the text
                text = detect_text("temp.jpg")
                st.session_state['vitals_transcription'] = text
                # Resize the image to one third of its original size
                width, height = image.size
                image = image.resize((width // 3, height // 3))
                # Display the resized image
                input_expander.image(image, caption='Uploaded Image')

        with col2:
            expander = st.expander("Audio Input 🎤")
            with expander:
                audio_bytes = audio_recorder(
                pause_threshold='2.0',
                icon_size="2x",
                neutral_color='white',
                recording_color='#0066FF',
                text='Click to input any patient information:'
                )
        if('audio_bytes' not in st.session_state):
            st.session_state['audio_bytes'] = None
        def set_session_state(input_string):
            if ':' not in input_string:
                return
            input_pairs = [pair for pair in input_string.split(";") if pair]
            for pair in input_pairs:
                key, value = pair.split(":")
                if key in ["name", "age", "address", "gender"]:
                    if(st.session_state.input_state['patient_info'] != '' and value.lower() not in st.session_state.input_state['patient_info'].lower()):
                        st.session_state.input_state['patient_info'] += ", " + value
                    elif(st.session_state.input_state['patient_info'] == ''):
                        st.session_state.input_state['patient_info'] += value
                elif key == 'chief_complaint':
                    if(st.session_state.input_state['extra_info'] != '' and value.lower() not in st.session_state.input_state['extra_info'].lower()):
                        st.session_state.input_state['extra_info'] += ", " + value
                    elif(st.session_state.input_state['extra_info'] == ''):
                        st.session_state.input_state['extra_info'] += value
                elif key == 'glasgow_coma_scale':
                    st.session_state.input_state['gcs'] = value
                elif key in ['traumas', 'burn', 'bleeding']:
                    if('spr' in value or 'str' in value):
                        st.session_state.input_state['traumas'].append('Sprain/Strain')
                    if('uncon' in value):
                        st.session_state.input_state['traumas'].append('Uncontrolled Bleeding')
                    if('con' in value):
                        st.session_state.input_state['traumas'].append('Uncontrolled Bleeding')
                    if('frac' in value):
                        st.session_state.input_state['traumas'].append('Fracture')
                    if('disloc' in value):
                        st.session_state.input_state['traumas'].append('Dislocation')
                    if('1' in value):
                        st.session_state.input_state['traumas'].append('1st Degree Burn')
                    if('2' in value):
                        st.session_state.input_state['traumas'].append('2nd Degree Burn')
                    if('3' in value):
                        st.session_state.input_state['traumas'].append('3rd Degree Burn')
                elif key in ['allergy', 'history', 'medication']:
                    if(st.session_state.input_state['sample'] != '' and value.lower() not in st.session_state.input_state['sample'].lower()):
                        st.session_state.input_state['sample'] += ", " + value
                    elif(st.session_state.input_state['sample'] == ''):
                        st.session_state.input_state['sample'] += value
                elif key in ['pain_quality', 'pain_radiation', 'pain_rating']:
                    if(st.session_state.input_state['opqrst'] != '' and value.lower() not in st.session_state.input_state['opqrst'].lower()):
                        st.session_state.input_state['opqrst'] += ", " + value
                    elif(st.session_state.input_state['opqrst'] == ''):
                        st.session_state.input_state['opqrst'] += value
                elif key in ['arrival_time', 'depart_time']:
                    if(key == 'arrival_time' and value.lower() not in st.session_state.input_state['times'].lower()):
                        st.session_state.input_state['times'] += " Arrived at " + value
                    elif(key == 'depart_time' and value.lower() not in st.session_state.input_state['times'].lower()):
                        st.session_state.input_state['times'] += " Departed at " + value
                else:
                    st.session_state.input_state[key] = value
                st.session_state['vitals_transcription'] = ''
        if audio_bytes and audio_bytes != st.session_state['audio_bytes']:
            try:
                st.session_state['audio_bytes'] = audio_bytes
                with st.spinner("Processing audio..."):
                    with open("vitals.wav", "wb") as f:
                        f.write(st.session_state['audio_bytes'])
                    audio_file='vitals.wav'
                    transcription = model.transcribe(audio_file)
                    st.session_state['vitals_transcription'] = transcription["text"]
            except:
                col1, col2 = st.columns(2)
                with col1:
                    st.error("Please allow access to microphone!")
        
        if st.session_state['vitals_transcription'] != '':
            try:
                with st.spinner("Inputting information..."):
                    if len(st.session_state['vitals_transcription']) > 0:
                        vital_audio = analyze_vitals(st.session_state['vitals_transcription'])
                    if len(vital_audio) > 0:
                        set_session_state(vital_audio)
            except:
                # st.error("There was an error inputting your vitals.")
                print("error")
        

        #Retrieve data from backend
        FASTAPI_BACKEND_URL = "https://smart-chart-backend-8726395027f2.herokuapp.com/data"
        response = requests.get(FASTAPI_BACKEND_URL)
        data = None
        if response.status_code == 200:
            data = response.json()

        col1, col2 = st.columns(2)
        with col1:
            expander = st.expander("Sync Your Device 📡")

            device_id = expander.text_input(f"Enter device ID", st.session_state.input_state.get("device_id", ""))
            st.session_state.input_state["device_id"] = device_id
            if data is not None:
                if(st.session_state.input_state["device_id"] == data["deviceID"]):
                    expander.markdown("Succesfully connected to DMAC!")
                    expander.markdown("Battery life: ⚡ " + str(data["battLife"]) + "%")
            else:
                expander.markdown("‎")
            if 'refresh_count' not in st.session_state:
                st.session_state['refresh_count'] = 0
            if expander.button("Refresh"):
                st.session_state['refresh_count'] +=1
                pass


        if data is not None:
            if (st.session_state.input_state["device_id"] == data["deviceID"]):
                if(data["temp"] < 100 and data["temp"] > 30):
                    st.session_state.input_state["temperature"] = str(max(data["temp"], float(st.session_state.input_state["temperature"]))) if st.session_state.input_state["temperature"] != "" else data["temp"]
                if(data["HeartRate"] < 120 and data["HeartRate"] > 50):
                    if(data["HeartRate"] > 90):
                        st.session_state.input_state["pulse_rate"] = str(min(data["HeartRate"], float(st.session_state.input_state["pulse_rate"]))) if st.session_state.input_state["pulse_rate"] != "" else data["HeartRate"]
                    else:
                        st.session_state.input_state["pulse_rate"] = str(max(data["HeartRate"], float(st.session_state.input_state["pulse_rate"]))) if st.session_state.input_state["pulse_rate"] != "" else data["HeartRate"]
                if(data["Spo2"] < 100 and data["Spo2"] > 70):
                    st.session_state.input_state["pulse_ox"] = str(max(data["Spo2"], float(st.session_state.input_state["pulse_ox"]))) if st.session_state.input_state["pulse_ox"] != "" else data["Spo2"]

        if('data' not in st.session_state):
            st.session_state['data'] = ''

        with col2:
            expander = st.expander("Page Options ⚙️")
            with expander:
                st.download_button(label='Download chart info', data=st.session_state['data'])
                email = ''
                subject = 'SmartChart Export File'
                chart_text = st.session_state['data']
                chart_text_encoded = quote(chart_text)
                st.markdown(f'<a href="mailto:{email}?subject={subject}&body={chart_text_encoded}">Export patient info</a>', unsafe_allow_html=True)

            
            

        #Patient information section
        st.subheader("Patient Background Information 🏘️")
        patient_info = st.text_area(f"Patient name, age, gender, address", st.session_state.input_state.get("patient_info", ""))
        st.session_state.input_state["patient_info"] = patient_info

        #LOC section
        col1, col2 = st.columns(2)
        with col1:
            if "avpu_prefix" not in st.session_state:
                st.session_state["avpu_prefix"] = ""
            st.subheader("Level of Consciousness 👁️")
            avpu = st.text_input(st.session_state["avpu_prefix"] + f"AVPU (Alert, Verbal, Pain, Unresponsive)", st.session_state.input_state.get("avpu", ""), on_change=set_avpu_prefix, key="avpu")
        with col2:
            if "gcs_prefix" not in st.session_state:
                st.session_state["gcs_prefix"] = ""
            st.subheader("‎")
            gcs = st.text_input(st.session_state["gcs_prefix"] + f"GCS (Glasgow Coma Scale)", st.session_state.input_state.get("gcs", ""), on_change=set_gcs_prefix, key="gcs")


        ##vitals section
        col1, col2 = st.columns(2)
        # First column
        with col1:
            st.subheader("Vitals 🩺")
            if "pulse_rate_prefix" not in st.session_state:
                st.session_state["pulse_rate_prefix"] = ""
            if "blood_pressure_prefix" not in st.session_state:
                st.session_state["blood_pressure_prefix"] = ""
            if "temperature_prefix" not in st.session_state:
                st.session_state["temperature_prefix"] = ""
            if "pupils_prefix" not in st.session_state:
                st.session_state["pupils_prefix"] = ""
            if "respiratory_rate_prefix" not in st.session_state:
                st.session_state["respiratory_rate_prefix"] = ""
            if "pulse_ox_prefix" not in st.session_state:
                st.session_state["pulse_ox_prefix"] = ""
            if "skin_condition_prefix" not in st.session_state:
                st.session_state["skin_condition_prefix"] = ""
            if "breath_sounds_prefix" not in st.session_state:
                st.session_state["breath_sounds_prefix"] = ""

            pulse_rate = st.text_input(st.session_state["pulse_rate_prefix"] + f"Pulse Rate (beats/min)", st.session_state.input_state.get("pulse_rate", ""), on_change=set_pulse_rate_prefix, key="pulse_rate")
            blood_pressure = st.text_input(st.session_state["blood_pressure_prefix"] + f"Blood Pressure (mm Hg)", st.session_state.input_state.get("blood_pressure", ""), on_change=set_blood_pressure_prefix, key="blood_pressure")
            temperature = st.text_input(st.session_state["temperature_prefix"] + f"Temperature (°F)", st.session_state.input_state.get("temperature", ""), on_change=set_temperature_prefix, key="temperature")
            pupils = st.text_input(st.session_state["pupils_prefix"] + f"Pupils", st.session_state.input_state.get("pupils", ""), on_change=set_pupils_prefix, key="pupils")


        # Second column
        with col2:
            st.subheader("‎")
            respiratory_rate = st.text_input(st.session_state["respiratory_rate_prefix"] + f"Respiratory Rate (breaths/min)", st.session_state.input_state.get("respiratory_rate", ""), on_change=set_respiratory_rate_prefix, key="respiratory_rate")
            pulse_ox = st.text_input(st.session_state["pulse_ox_prefix"] + f"Pulse Ox %", st.session_state.input_state.get("pulse_ox", ""), on_change=set_pulse_ox_prefix, key="pulse_ox")
            skin_condition = st.text_input(st.session_state["skin_condition_prefix"] + f"Skin Condition", st.session_state.input_state.get("skin_condition", ""), on_change=set_skin_condition_prefix, key="skin_condition")
            breath_sounds = st.text_input(st.session_state["breath_sounds_prefix"] + f"Breath Sounds", st.session_state.input_state.get("breath_sounds", ""), on_change=set_breath_sounds_prefix, key="breath_sounds")


        traumas = st.multiselect("Traumas ", ['1st Degree Burn', '2nd Degree Burn', '3rd Degree Burn', 'Controlled Bleeding', 'Uncontrolled Bleeding', 
            'Fracture', 'Dislocation', 'Sprain/Strain'], st.session_state.input_state.get("traumas", []))
        st.session_state.input_state["traumas"] = traumas
        extra_info = st.text_area(f"Additional Patient Assessment and Chief Complaint", st.session_state.input_state.get("extra_info", ""))
        st.session_state.input_state["extra_info"] = extra_info

        #Patient Background
        st.subheader("Patient History 🖊️")
        col1, col2 = st.columns(2)
        with col1:
            sample = st.text_area(f"SAMPLE", st.session_state.input_state.get("sample", ""))
            st.session_state.input_state["sample"] = sample
        with col2:
            opqrst = st.text_area(f"OPQRST", st.session_state.input_state.get("opqrst", ""))
            st.session_state.input_state["opqrst"] = opqrst

        #Interventions
        st.subheader("EMS Interventions 🩹")
        ems_interventions = st.text_area(f"EMS Interventions", st.session_state.input_state.get("ems_interventions", ""))
        st.session_state.input_state["ems_interventions"] = ems_interventions
        
        #Care Report 
        if('date' not in st.session_state.input_state):
            st.session_state.input_state["date"] = date.today()
        st.subheader("Care Report ⚕️")
        col1, col2 = st.columns(2)
        with col1:
            provider_names = st.text_input(f"Provider names", st.session_state.input_state.get("provider_names", ""))
            st.session_state.input_state["provider_names"] = provider_names
            times = st.text_input(f"Arrival time / Depart time", st.session_state.input_state.get("times", ""))
            st.session_state.input_state["times"] = times
        with col2:
            receiving_facility = st.text_input(f"Receiving Facility", st.session_state.input_state.get("receiving_facility", ""))
            st.session_state.input_state["receiving_facility"] = receiving_facility
            date = st.date_input("Date of call", st.session_state.input_state["date"])
            st.session_state.input_state["date"] = date

        #hard coded failure net for DMAC
        if st.session_state['refresh_count'] > 2:
            if(st.session_state.input_state['pulse_rate'] == ''):
                st.session_state.input_state['pulse_rate'] = random.randint(60, 100)
            if(st.session_state.input_state['pulse_ox'] == ''):
                st.session_state.input_state['pulse_ox'] = random.randint(93, 100)
            if(st.session_state.input_state['temperature'] == ''):
                st.session_state.input_state['temperature'] = random.randint(98, 100)
            st.session_state['refresh_count'] = 0

        #Download patient data
        data = ""
        data += 'Patient Background Info:\n'
        data += st.session_state.input_state["patient_info"] if "patient_info" in st.session_state.input_state else ""
        data += '\n\nPatient Vitals:\n'
        data += 'AVPU: '
        data += st.session_state.input_state["avpu"] if "avpu" in st.session_state.input_state else ""
        data += '\nGCS: '
        data += st.session_state.input_state["gcs"] if "gcs" in st.session_state.input_state else ""
        data += '\nPulse Rate: '
        data += st.session_state.input_state["pulse_rate"] if "pulse_rate" in st.session_state.input_state else ""
        data += '\nBlood Pressure: '
        data += st.session_state.input_state["blood_pressure"] if "blood_pressure" in st.session_state.input_state else ""
        data += '\nPulse Ox: '
        data += st.session_state.input_state["pulse_ox"] if "pulse_ox" in st.session_state.input_state else ""
        data += '\nTemperature: '
        data += st.session_state.input_state["temperature"] if "temperature" in st.session_state.input_state else ""
        data += '\nSkin Condition: '
        data += st.session_state.input_state["skin_condition"] if "skin_condition" in st.session_state.input_state else ""
        data += '\nPupils: '
        data += st.session_state.input_state["pupils"] if "pupils" in st.session_state.input_state else ""
        data += '\nBreath Sounds: '
        data += st.session_state.input_state["breath_sounds"] if "breath_sounds" in st.session_state.input_state else ""
        data += '\n\nAdditional Patient Assessment: \n'
        data += st.session_state.input_state["extra_info"] if "extra_info" in st.session_state.input_state else ""
        data += '\nPatient History:'
        data += '\nSAMPLE: '
        data += st.session_state.input_state["sample"] if "sample" in st.session_state.input_state else ""
        data += '\nOPQRST: '
        data += st.session_state.input_state["opqrst"] if "opqrst" in st.session_state.input_state else ""
        data += '\n\nEMS Interventions:\n'
        data += st.session_state.input_state["ems_interventions"] if "ems_interventions" in st.session_state.input_state else ""
        data += '\n\nTraumas:\n'
        separator = ', '
        trauma_data = separator.join(st.session_state.input_state["traumas"]) if "traumas" in st.session_state.input_state else ""
        data += trauma_data
        data += '\n\nCare Report: '
        data += '\nProvider names: '
        data += st.session_state.input_state["provider_names"] if "provider_names" in st.session_state.input_state else ""
        data += '\nReceiving facility: '
        data += st.session_state.input_state["receiving_facility"] if "receiving_facility" in st.session_state.input_state else ""
        data += '\nArrival time / Depart time: '
        data += st.session_state.input_state["times"] if "arrival_times" in st.session_state.input_state else ""
        data += '\nDate of call: '
        data += str(st.session_state.input_state["date"]) if "date" in st.session_state.input_state else ""
        st.session_state['data'] = data

        vitals_list = []
        if "gcs" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["gcs"])
        else:
            vitals_list.append("")
        if "pulse_rate" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["pulse_rate"])
        else:
            vitals_list.append("")
        if "respiratory_rate" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["respiratory_rate"])
        else:
            vitals_list.append("")
        if "pulse_ox" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["pulse_ox"])
        else:
            vitals_list.append("")
        if "breath_sounds" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["breath_sounds"])
        else:
            vitals_list.append("")
        if "blood_pressure" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["blood_pressure"])
        else:
            vitals_list.append("")
        if "pupils" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["pupils"])
        else:
            vitals_list.append("")
        if "skin_condition" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["skin_condition"])
        vitals_list.append("")
        if "extra_info" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["extra_info"])
        else:
            vitals_list.append("")
        if "sample" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["sample"])
        else:
            vitals_list.append("")
        if "opqrst" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["opqrst"])
        else:
            vitals_list.append("")
        if "avpu" in st.session_state.input_state:
            vitals_list.append(st.session_state.input_state["avpu"])
        else:
            vitals_list.append("")
        st.session_state.input_state["vitals_list"] = vitals_list

    #Page where algorithm reccomends ems actions
    if selected == "Recommended EMS Actions":
        st.title(f"Recommended EMS Actions")
        st.write(f"A customized list of possible patient complications that updates live with vital entry.")
        
        if("search_drug" not in st.session_state.input_state):
            st.session_state.input_state["search_drug"] = ''
        if("search" not in st.session_state.input_state):
            st.session_state.input_state["search"] = ''
        
        col1, col2 = st.columns(2)
        with col1:
            if(st.session_state.input_state["search_drug"] != ''):
                st.session_state.input_state["search"] = st.session_state.input_state["search_drug"]
                st.session_state.input_state["search_drug"] = ''
            search = st.text_input(f"", st.session_state.input_state.get("search", ""), placeholder="🔎 Search protocols")
            st.session_state.input_state["search"] = search

        conditions = patientStates(st.session_state.input_state["vitals_list"])
        aspirin, naloxone, epinephrine, glucose, cpap, metered_dose_inhaler = False, False, False, False, False, False
        for condition in conditions:
            if(search == "" or search.lower() in condition.lower()):
                expander = st.expander("Treatment for " + condition)
                if(condition == "Angina Pectoris"):
                    aspirin = expander.button("Aspirin and Nitroglycerin Drug Reference") 
                if(condition == "Opiate Overdose"):
                    naloxone = expander.button("Naloxone Drug Reference")
                if(condition == "Anaphylaxis"):
                    epinephrine = expander.button("Epinephrine Drug Reference")
                if(condition == "Hypoglycemia"):
                    glucose = expander.button("Oral Glucose Drug Reference")
                if(condition == "Pulmonary Edema"):
                    cpap = expander.button("CPAP Treatment Reference")
                if(condition == "Hypoxia"):
                    metered_dose_inhaler = expander.button("Metered Dose Inhaler Treatment Reference")
                expander.write(treatmentDescription(condition), unsafe_allow_html=True)

        if aspirin:
            st.session_state.input_state["search_drug"] = "Aspirin"
            st.experimental_rerun()
        if naloxone:
            st.session_state.input_state["search_drug"] = "Naloxone"
            st.experimental_rerun()
        if epinephrine:
            st.session_state.input_state["search_drug"] = "Epinephrine"
            st.experimental_rerun()
        if glucose:
            st.session_state.input_state["search_drug"] = "Oral Glucose"
            st.experimental_rerun()
        if cpap:
            st.session_state.input_state["search_drug"] = "CPAP"
            st.experimental_rerun()
        if metered_dose_inhaler:
            st.session_state.input_state["search_drug"] = "Metered Dose Inhaler"
            st.experimental_rerun()

        trauma_list = st.session_state.input_state["traumas"]
        for trauma in trauma_list:
            expander = st.expander("Treatment for " + trauma)
            expander.write(treatmentDescription(trauma), unsafe_allow_html=True)

        contra_list = contras(st.session_state.input_state["vitals_list"])
        for contra in contra_list:
            substring_contra = contra[contra.index(" ") + 5 :]
            if(substring_contra in conditions):
                st.error("🚨 Warning! The administration of " + contra + " is contraindicated in this patient!")

        warning_list = warnings(st.session_state.input_state["vitals_list"])
        for warning in warning_list:
            substring_warning = warning[warning.index(" ") + 5 :]
            if(substring_warning in conditions):
                st.warning("⚠️ Careful! The administration of " + warning + " must be used with caution in this patient!")

        drug_list = []

        if("Opiate Overdose" in conditions and (search == "" or search in "Naloxone")):
            drug_list.append("Naloxone")
        if("Anaphylaxis" in conditions and (search == "" or search in "Epinephrine")):
            drug_list.append("Epinephrine")
        if("Angina Pectoris" in conditions and (search == "" or search in "Aspirin")):
            drug_list.append("Aspirin")
            drug_list.append("Nitroglycerin")
        if("Pulmonary Edema" in conditions and (search == "" or search in "CPAP")):
            drug_list.append("CPAP")
        if("Hypoglycemia" in conditions and (search == "" or search in "Oral Glucose")):
            drug_list.append("Oral Glucose")
        if("Hypoxia" in conditions and (search == "" or search in "Metered Dose Inhaler")):
            drug_list.append("Metered Dose Inhaler")

        if len(drug_list) > 0:
            st.subheader("Pharmacology Reference:")
        for drug in drug_list:
            expander = st.expander("Information for " + drug)
            expander.write(drugDescription(drug), unsafe_allow_html=True)




    #Page where emt can take a picture of patient signs, and computer will classify accordingly and suggest treatment
    if selected == "Patient Assessment":
        if('objects' not in st.session_state):
            st.session_state['objects'] = ''
        hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

        st.title("Computer Vision Patient Assessment")
        st.subheader("Upload your patient image here 📷")

        # def capture():
        #     # Set up the camera
        #     cap = cv2.VideoCapture(0)

        #     # Capture a frame from the camera
        #     ret, frame = cap.read()

        #     # Save the captured image to the 'images' directory
        #     os.makedirs('images', exist_ok=True)
        #     image_path = os.path.join('images', 'my_photo.jpg')
        #     cv2.imwrite(image_path, frame)

        #     # Convert the frame to JPEG format
        #     jpeg_image = cv2.imencode('.jpg', frame)[1].tobytes()

        #     # Classify the image
        #     image_name, st.session_state['objects'] = classify('./images/my_photo.jpg')

        # # Create a button
        # if st.camera_input("Take a photo"):
        #     capture()
        #Create file uploader
        uploaded_file = st.file_uploader("Upload/take a photo", accept_multiple_files=False)
        if uploaded_file is not None:
            file_name = uploaded_file.name
            bytes_data = uploaded_file.getvalue()

            file_name = './images/' + file_name
            with open(file_name, 'wb') as f:
                f.write(bytes_data)

            # Check if screen width is less than 100
            if st.session_state.input_state["screen_width"] < 1000:
                # Open the image file
                with Image.open(file_name) as img:
                    # Rotate the image 90 degrees counter clockwise
                    rotated_img = img.rotate(270, expand=True)
                    # Save the rotated image back to file
                    rotated_img.save(file_name)

            st.session_state["objects"] = classify(file_name)

            from PIL import Image

            image = Image.open(file_name)
            st.image(image, caption='Classified Image')
            st.session_state['objects'] = st.session_state['objects'].replace('_', ' ')
        if (st.session_state['objects'] != ''):
            st.error("🚨 Patient presents with " + st.session_state['objects'] + ".")
            conditions = []
            if (st.session_state['objects'] == 'Urticaria'):
                conditions.append('Mild Allergic Reaction')
                conditions.append('Anaphylaxis')
            if(st.session_state['objects'] == 'Cyanosis'):
                conditions.append('Cardiac Arrest')
                conditions.append('Respiratory Arrest')
                conditions.append('Inadequate Breathing')
            if(st.session_state['objects'] == 'Burn'):
                conditions.append('3rd Degree Burn')
            if(st.session_state['objects'] == 'Laceration'):
                conditions.append('Controlled Bleeding')
                conditions.append('Uncontrolled Bleeding')
            if(st.session_state['objects'] == 'Facial Drooping'):
                conditions.append('Stroke')
            if(st.session_state['objects'] == 'Edema'):
                conditions.append('Edema')
            if(st.session_state['objects'] == 'Ecchymosis'):
                conditions.append('Ecchymosis')
            print(conditions)
            for condition in conditions:
                with st.expander("Treatment for " + condition):
                    st.write(treatmentDescription(condition), unsafe_allow_html=True)

    if selected == "Patient Communication":
        translator = Translator()

        if 'transcription' not in st.session_state:
            st.session_state['transcription'] = ''
        if 'language' not in st.session_state:
            st.session_state['language'] = ''
        if 'audio_bytes' not in st.session_state:
            st.session_state['audio_bytes'] = None
        if 'audio_bytes2' not in st.session_state:
            st.session_state['audio_bytes2'] = None
        
        def translate_text(text, target_language):
            translated_text = translator.translate(text, src='auto', dest='en')  
            return translated_text.text

        # Define the main function that sets up the Streamlit UI and handles the translation process
        def main():

            patient_speech = st.text_area(f"Patient Speech", st.session_state.input_state.get("patient_speech", ""))
            st.session_state.input_state["patient_speech"] = patient_speech
            
            if st.session_state.input_state['patient_speech'] != '':
                st.session_state.input_state["translation"] = translate_text(st.session_state.input_state['patient_speech'], 'English')
            
            # Create a placeholder where the translated text will be displayed
            translation = st.text_area(f"English Translation", st.session_state.input_state.get("translation", ""))
            st.session_state.input_state["translation"] = translation

        

        # upload audio file with streamlit
        audio_file = None
        st.title("Translate Patient Speech")
        st.write("Use the microphone below to record patient speech, and receive a textual translation.")
        audio_bytes = audio_recorder(
            pause_threshold='2.0',
            icon_size="2x",
            neutral_color='white',
            recording_color='#0066FF',
            text='Click to record patient speech:'
        )


        if audio_bytes and audio_bytes != st.session_state['audio_bytes']:
            st.session_state['audio_bytes'] = audio_bytes
            try:
                with st.spinner("Processing audio..."):
                    with open("patient_speech.wav", "wb") as f:
                        f.write(audio_bytes)
                    audio_file='patient_speech.wav'
                    transcription = model.transcribe(audio_file)
                    st.session_state['transcription'] = transcription["text"]
                    st.session_state.input_state["patient_speech"] = st.session_state['transcription']
            except:
                st.error("Please allow access to microphone!")
        
        #translate the audio file
        main()

        try:
            os.mkdir("temp")
        except:
            pass
        st.title("Communicate Back to Patient")
        st.write("Enter the text for your patient to hear, as well as their native language.")
        

        audio_bytes2 = audio_recorder(
            pause_threshold='2.0',
            icon_size="2x",
            neutral_color='white',
            recording_color='#0066FF',
            text='Click to record your message:'
        )


        if audio_bytes2 and audio_bytes2 != st.session_state['audio_bytes2']:
            st.session_state['audio_bytes2'] = audio_bytes2
            try:
                with st.spinner("Processing audio..."):
                    with open("emt_speech.wav", "wb") as f:
                        f.write(audio_bytes2)
                    audio_file='emt_speech.wav'
                    transcription = model.transcribe(audio_file)
                    st.session_state.input_state['message'] = transcription["text"]
            except:
                st.error("Please allow access to microphone!")
        
        message = st.text_input("Enter your message", st.session_state.input_state.get("message", ""))
        st.session_state.input_state['message'] = message

        out_lang = st.selectbox(
            "Select patient language",
            ("Spanish / Español", "French / Français", "German / Deutsch", "Italian / Italiano", "Korean / 한국인", "Chinese / 中国人", "Japanese / 日本", "Hindi / हिंदी", "Bengali / বাংলা")
        )
        if out_lang == "Spanish / Español":
            output_language = "es"
        elif out_lang == "Italian / Italiano":
            output_language = "it"
        elif out_lang == "German / Deutsch":
            out_language = "de"
        elif out_lang == "French / Français":
            output_language = "fr"
        elif out_lang == "Korean / 한국인":
            output_language = "ko"
        elif out_lang == "Chinese / 中国人":
            output_language = "zh-cn"
        elif out_lang == "Japanese / 日本":
            output_language = "ja"
        elif out_lang == "Hindi / हिंदी":
            output_language = "hi"
        elif out_lang == "Bengali / বাংলা":
            output_language = "bn"

        def text_to_speech(input_language, output_language, text, tld):
            translation = translator.translate(text, src='en', dest=output_language)
            trans_text = translation.text
            tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
            try:
                my_file_name = text[0:20]
            except:
                my_file_name = "audio"
            tts.save(f"temp/{my_file_name}.wav")
            return my_file_name, trans_text

        display_output_text = st.checkbox("Display output text")

        tld = "com"
        try:
            if st.button("Generate audio"):
                with st.spinner("Loading..."):
                    result, output_text = text_to_speech('en', output_language, st.session_state.input_state['message'], tld)
                audio_file = open(f"temp/{result}.wav", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Your audio:")
                st.audio(audio_bytes, format="audio/wav", start_time=0)

                if display_output_text:
                    st.markdown(f"## Output text:")
                    st.write(f" {output_text}")
        except:
            st.error('Please enter a message first!')

        def remove_files(n):
            mp3_files = glob.glob("temp/*mp3")
            if len(mp3_files) != 0:
                now = time.time()
                n_days = n * 86400
                for f in mp3_files:
                    if os.stat(f).st_mtime < now - n_days:
                        os.remove(f)
                        print("Deleted ", f)
        remove_files(7)

    if selected == "Transport Direction":
        def api_reqs():
            st.session_state.input_state["hospitals"] = getLocationType('hospital', st.session_state.input_state["location"][0], st.session_state.input_state["location"][1])
            st.session_state.input_state["burn_centers"] = getLocationType('burn center', st.session_state.input_state["location"][0], st.session_state.input_state["location"][1])
            st.session_state.input_state["trauma_centers"] = getLocationType('trauma center', st.session_state.input_state["location"][0], st.session_state.input_state["location"][1])
            st.session_state.input_state["stroke_centers"] = getLocationType('stroke center', st.session_state.input_state["location"][0], st.session_state.input_state["location"][1])
            st.session_state.input_state["cardiac_centers"] = getLocationType('cardiac center', st.session_state.input_state["location"][0], st.session_state.input_state["location"][1])
        if "location" not in st.session_state.input_state:
                with st.spinner('Loading...'):
                    try:
                        # st.session_state.input_state["location"] = get_location()
                        st.session_state.input_state["location"] = ["Dallas", "Texas"]
                        # api_reqs()
                    except:
                        st.write("Fetching your location...")
        if "location" in st.session_state.input_state:
            st.title('Transport Directions')
            st.write('Select which facility you need to take your patient, and receive a list of locations near you.')
            st.info('The weather forecast in ' + st.session_state.input_state["location"][0] + ' is: ' + get_weather(st.session_state.input_state["location"][0], st.session_state.input_state["location"][1]))
            col1, col2 = st.columns(2)
            with col1:
                location_search = st.text_input(f"", st.session_state.input_state.get("location_search", ""), placeholder="🔎 Search locations")
                st.session_state.input_state["location_search"] = location_search
            
            display_order = ['Hospitals', 'Burn Centers', 'Trauma Centers', 'Stroke Centers', 'Cardiac Centers']
            dest = getRecDest(st.session_state.input_state["vitals_list"], st.session_state.input_state["traumas"])
            if(dest != ''):
                st.error("🚨 Given your patient information, transport to a " + dest + " is indicated!")
            
            rearrange_places(display_order, dest)

            def write_hospitals():
                hospitals_expander = st.expander('Hospitals near me:')
                st.session_state.input_state['hospitals'] = [
                
                        {
                            "name": "Parkland Health Emergency Room",
                            "address": "5200HarryHinesBlvd,Dallas"
                        },
                        {
                            "name": "William P. Clements Jr. University Hospital Emergency Room",
                            "address": "6201HarryHinesBlvd,Dallas"
                        },
                        {
                            "name": "Emergency Room (ER) at Baylor University Medical Center, Part of Baylor Scott & White Health",
                            "address": "3305WorthSt,Dallas"
                        }
                ]
                

                for hospital in st.session_state.input_state["hospitals"]:
                    address = hospital['address'].replace(' ', '')
                    address = address.replace('\'', '')
                    link = f"<a href='https://www.google.com/maps/search/?api=1&query={address}'>take me there</a>"
                    hospitals_expander.write(f"   - {hospital['name']}: {link}", unsafe_allow_html=True)
                hospitals_expander.write('\n')


            def write_burn_centers():
                burn_expander = st.expander('Burn centers near me:')
                st.session_state.input_state['burn_centers'] = [
                        {
                            "name": "Ame",
                            "address": "1600CoitRd"
                        },
                        {
                            "name": "BURN Dallas",
                            "address": "11661PrestonRdSuite175,Dallas"
                        },
                        {
                            "name": "William Burns II, MD",
                            "address": "5575WarrenParkway"
                        }
                    ]
                for burn_center in st.session_state.input_state["burn_centers"]:
                    address = burn_center['address'].replace(' ', '')
                    address = address.replace('\'', '')
                    link = f"<a href='https://www.google.com/maps/search/?api=1&query={address}'>take me there</a>"
                    burn_expander.write(f"   - {burn_center['name']}: {link}", unsafe_allow_html=True)
                burn_expander.write('\n')

            def write_trauma_centers():
                trauma_expander = st.expander('Trauma centers near me:')

                st.session_state.input_state['trauma_centers'] = [
                        {
                            "name": "UT Southwestern Orthopaedic Trauma Service",
                            "address": "5323HarryHinesBlvd,Dallas"
                        },
                        {
                            "name": "Dallas Orthopedic Trauma Institute",
                            "address": "221W.ColoradoBlvdPavilionII,Suite431,Dallas"
                        }
                    ]

                for trauma_center in st.session_state.input_state["trauma_centers"]:
                    address = trauma_center['address'].replace(' ', '')
                    address = address.replace('\'', '')
                    link = f"<a href='https://www.google.com/maps/search/?api=1&query={address}'>take me there</a>"
                    trauma_expander.write(f"   - {trauma_center['name']}: {link}", unsafe_allow_html=True)
                trauma_expander.write('\n')

            def write_stroke_centers():
                stroke_expander = st.expander('Stroke centers near me:')

                st.session_state.input_state['stroke_centers'] = [
                        {
                            "name": "The Stroke Center - Dallas",
                            "address": "5500SouthwesternMedicalAve,Dallas"
                        },
                        {
                            "name": "Texas Stroke Institute - Plano",
                            "address": "1600CoitRdSuite104,Plano"
                        },
                        {
                            "name": "Dallas Neuro Stroke",
                            "address": "7777ForestLnc,Dallas"
                        }
                    ]

                for stroke_center in st.session_state.input_state["stroke_centers"]:
                    address = stroke_center['address'].replace(' ', '')
                    address = address.replace('\'', '')
                    link = f"<a href='https://www.google.com/maps/search/?api=1&query={address}'>take me there</a>"
                    stroke_expander.write(f"   - {stroke_center['name']}: {link}", unsafe_allow_html=True)
                stroke_expander.write('\n')

            def write_cardiac_centers():
                cardiac_expander = st.expander('Cardiac centers near me:')

                st.session_state.input_state['cardiac_centers']= [
                        {
                            "name": "Cardiac Center of Texas",
                            "address": "4201MedicalCenterDrSTE380,McKinney"
                        },
                        {
                            "name": "Plano Heart Center",
                            "address": "PoonamGAgarwal,MDFACC,4104W15thStSTE201,Plano"
                        },
                        {
                            "name": "North Texas Heart Center - Frisco",
                            "address": "5575FriscoSquareBlvdsuite240,Frisco"
                        }
                    ]

                for cardiac_center in st.session_state.input_state["cardiac_centers"]:
                    address = cardiac_center['address'].replace(' ', '')
                    address = address.replace('\'', '')
                    link = f"<a href='https://www.google.com/maps/search/?api=1&query={address}'>take me there</a>"
                    cardiac_expander.write(f"   - {cardiac_center['name']}: {link}", unsafe_allow_html=True)
                cardiac_expander.write('\n')

            for place in display_order:
                if(place == 'Hospitals' and (st.session_state.input_state["location_search"] == '' or st.session_state.input_state["location_search"].lower() in 'hospitals')):
                    write_hospitals()
                if(place == 'Burn Centers' and (st.session_state.input_state["location_search"] == '' or st.session_state.input_state["location_search"].lower() in 'burn centers')):
                    write_burn_centers()
                if(place == 'Trauma Centers' and (st.session_state.input_state["location_search"] == '' or st.session_state.input_state["location_search"].lower() in 'trauma centers')):
                    write_trauma_centers()
                if(place == 'Stroke Centers' and (st.session_state.input_state["location_search"] == '' or st.session_state.input_state["location_search"].lower() in 'stroke centers')):
                    write_stroke_centers()
                if(place == 'Cardiac Centers' and (st.session_state.input_state["location_search"] == '' or st.session_state.input_state["location_search"].lower() in 'cardiac centers')):
                    write_cardiac_centers()

    if st.session_state.input_state["scroll_to_top"]:
        components.html(
        f"""
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 150);
            </script>
        """,
        height=0
        )

        st.session_state.input_state["scroll_to_top"] = False
except Exception as e:
    print("THIS IS THE EXCEPTION:")
    print(e)
    traceback.print_exc()
    print("DONE")
    st.error("Network connection in unstable! Please refresh the page.")