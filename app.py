import streamlit as st
import subprocess
import cv2
from detector import run_detector

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI TELE FR System",
    page_icon="🛡",
    layout="wide"
)

# ---------------------------------
# CSS
# ---------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#020617,
#0f172a,
#111827
);
}

/* Hide Streamlit Elements */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Title */
.title{
text-align:center;
font-size:32px;
font-weight:700;
color:white;
margin-top:-10px;
margin-bottom:5px;
}

/* Subtitle */
.subtitle{
text-align:center;
font-size:14px;
color:#94a3b8;
margin-bottom:25px;
}

/* Buttons */
.stButton{
display:flex;
justify-content:center;
}

.stButton button{
width:180px;
height:45px;
font-size:14px;
font-weight:600;
border:none;
border-radius:10px;
color:white;

background:linear-gradient(
90deg,
#2563eb,
#7c3aed
);
}

.stButton button:hover{
transform:scale(1.03);
transition:0.2s;
}

/* Camera Header */
.camera-box{
background:#111827;
padding:10px;
border-radius:12px;
border:1px solid #334155;
margin-bottom:10px;
}

.camera-box h2{
font-size:18px;
color:white;
text-align:center;
margin:0;
}

/* Dashboard Cards */
.metric{
background:#111827;
padding:15px;
border-radius:12px;
border:1px solid #334155;
text-align:center;
color:white;
font-size:15px;
}

.metric b{
font-size:24px;
color:#38bdf8;
}

/* Camera Feed */
[data-testid="stImage"] img{
max-width:850px !important;
margin:auto;
display:block;
border-radius:15px;
border:2px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# TITLE
# ---------------------------------

st.markdown(
    '<div class="title">🛡 AI FR System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Face Recognition • Telegram Alerts • Live Monitoring</div>',
    unsafe_allow_html=True
)

# ---------------------------------
# BUTTONS
# ---------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    dataset_btn = st.button("DATASET")

with col2:
    train_btn = st.button(" TRAIN")

with col3:
    detect_btn = st.button(" DETECTOR")

# ---------------------------------
# BUTTON ACTIONS
# ---------------------------------

if dataset_btn:

    st.success("Dataset Creator Started")

    subprocess.run(
        ["python", "dataset_creator.py"]
    )

if train_btn:

    st.info("Training Model...")

    subprocess.run(
        ["python", "trainer.py"]
    )

    st.success("Training Completed")

# ---------------------------------
# CAMERA SECTION
# ---------------------------------

st.markdown("""
<div class="camera-box">
<h2>🎥 Live Surveillance Feed</h2>
</div>
""", unsafe_allow_html=True)

camera_col1, camera_col2, camera_col3 = st.columns([1,4,1])

with camera_col2:
    camera_placeholder = st.empty()

# ---------------------------------
# DETECTOR
# ---------------------------------

if "detecting" not in st.session_state:
    st.session_state.detecting = False

if detect_btn:
    st.session_state.detecting = True

if st.session_state.detecting:

    stop_btn = st.button("🛑 STOP DETECTOR")

    cap = cv2.VideoCapture(2)

    if not cap.isOpened():

        st.error("Camera Not Found")

    else:

        frame_window = st.empty()

        while st.session_state.detecting:

            ret, frame = cap.read()

            if not ret:
                st.error("Failed to Read Camera")
                break

            # Face Recognition + Telegram Alert
            frame = run_detector(
                frame,
                cap
            )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame_window.image(
                frame,
                channels="RGB",
                width=700
            )

            if stop_btn:
                st.session_state.detecting = False
                break

        cap.release()

# ---------------------------------
# DASHBOARD
# ---------------------------------

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric">
    📷 Dataset Images
    <br><br>
    <b>20</b>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric">
    Recognized Faces
    <br><br>
    <b>0</b>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric">
     Telegram Alerts
    <br><br>
    <b>0</b>
    </div>
    """, unsafe_allow_html=True)