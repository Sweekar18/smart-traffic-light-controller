import cv2
import numpy as np
import tempfile
import streamlit as st
import time

# Streamlit app title
st.title("🚦 Smart Traffic Light Controller")

# Upload 4 videos (North, East, South, West)
st.sidebar.header("Upload Traffic Videos")
north_file = st.sidebar.file_uploader("North", type=["mp4", "avi", "mov"])
east_file = st.sidebar.file_uploader("East", type=["mp4", "avi", "mov"])
south_file = st.sidebar.file_uploader("South", type=["mp4", "avi", "mov"])
west_file = st.sidebar.file_uploader("West", type=["mp4", "avi", "mov"])

# Store videos in temp files for OpenCV
def save_temp_file(uploaded_file):
    if uploaded_file is None:
        return None
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(uploaded_file.read())
    return temp.name

north_path = save_temp_file(north_file)
east_path = save_temp_file(east_file)
south_path = save_temp_file(south_file)
west_path = save_temp_file(west_file)

# Initialize video captures
caps = {}
if north_path: caps["North"] = cv2.VideoCapture(north_path)
if east_path: caps["East"] = cv2.VideoCapture(east_path)
if south_path: caps["South"] = cv2.VideoCapture(south_path)
if west_path: caps["West"] = cv2.VideoCapture(west_path)

# Streamlit UI controls
st.sidebar.header("Controls")
run_simulation = st.sidebar.checkbox("▶️ Start Simulation")
speed = st.sidebar.slider("Simulation Speed (seconds/frame)", 0.01, 1.0, 0.1, 0.01)
reset = st.sidebar.button("🔄 Reset Simulation")

# State management
if "frame_idx" not in st.session_state or reset:
    st.session_state.frame_idx = 0

# Placeholders for video display (2x2 grid)
col1, col2 = st.columns(2)
north_placeholder = col1.empty()
east_placeholder = col2.empty()
south_placeholder = col1.empty()
west_placeholder = col2.empty()

def read_frame(cap):
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
    return np.zeros((240, 320, 3), dtype=np.uint8)  # black if missing

# Simulation loop
if run_simulation and caps:
    while True:
        frames = {
            "North": read_frame(caps.get("North")),
            "East": read_frame(caps.get("East")),
            "South": read_frame(caps.get("South")),
            "West": read_frame(caps.get("West")),
        }

        # Display in grid
        north_placeholder.image(frames["North"], caption="North")
        east_placeholder.image(frames["East"], caption="East")
        south_placeholder.image(frames["South"], caption="South")
        west_placeholder.image(frames["West"], caption="West")

        st.session_state.frame_idx += 1
        time.sleep(speed)
