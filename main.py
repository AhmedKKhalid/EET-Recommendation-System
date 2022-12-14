import pyrebase
import streamlit as st
import recommender
from datetime import datetime
from pathlib import Path
from PIL import Image
st.set_page_config(layout="wide")

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
print(Path(__file__).parent)
config = current_dir/'.streamlit'/'config.toml'
with open(config, 'r'):
    print("done")
firebaseConfig = {
    'apiKey': "AIzaSyCxPTtrwqn4gRpK4ewLgTuF4mNiuJ6f5VI",
    'authDomain': "recommendation-system-eet.firebaseapp.com",
    'databaseURL': "https://recommendation-system-eet-default-rtdb.firebaseio.com",
    'projectId': "recommendation-system-eet",
    'storageBucket': "recommendation-system-eet.appspot.com",
    'messagingSenderId': "503909398932",
    'appId': "1:503909398932:web:55b2bdf784975d7395f781",
    'measurementId': "G-CVKHRMC2M9"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# Database
db = firebase.database()
storage = firebase.storage()
img_path = current_dir/"logo.png"
image = Image.open(img_path)
st.sidebar.image(image, width=300)

st.title("EET Global Hotel Recommender System")

# Authentication
# Obtain User Input for email and password

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

# App
# Login BlocklocalId

login = st.sidebar.checkbox('Login')
if login:
    try:
      user = auth.sign_in_with_email_and_password(email, password)
      recommender.recommender_system()

    except Exception as e:
        print(e)
        err_msg = '<p style="font-family:Courier; color:Red; font-size: 20px;">Please check email or password again !</p>'
        st.markdown(err_msg, unsafe_allow_html=True)
    st.sidebar.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)



