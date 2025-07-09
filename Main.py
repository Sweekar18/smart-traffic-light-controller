import cv2
import numpy as np
from time import sleep
import time

# Your original constants
largura_min = 80
altura_min = 80
offset = 6
pos_linha = 550
delay = 60

# Directions and setup
directions = ['North', 'East', 'South', 'West']
caps = {d: cv2.VideoCapture(f'{d.lower()}.mp4') for d in directions}
subtractors = {d: cv2.bgsegm.createBackgroundSubtractorMOG() for d in directions}
detecs = {d: [] for d in directions}
carros = {d: 0 for d in directions}

# Signal control
signal_state = 'NS'
signal_start_time = time.time()
last_vehicle_time = time.time()

# Center calculation
def pega_centro(x, y, w, h):
    cx = x + int(w / 2)
    cy = y + int(h / 2)
    return cx, cy

# Frame processing
def process_frame(frame, subtractor, detec, count):
    tempo = float(1 / delay)
    sleep(tempo)

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = subtractor.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    contorno, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)

    vehicles_passed = 0
    for c in contorno:
        x, y, w, h = cv2.boundingRect(c)
        if w >= largura_min and h >= altura_min:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame, centro, 4, (0, 0, 255), -1)

    for (x, y) in detec[:]:
        if pos_linha - offset < y < pos_linha + offset:
            count += 1
            vehicles_passed += 1
            cv2.line(frame, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
            detec.remove((x, y))

    cv2.putText(frame, "VEHICLE COUNT: " + str(count), (450, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    return frame, count, vehicles_passed

# Signal annotation
def annotate_signal(frame, is_green, direction):
    color = (0, 255, 0) if is_green else (0, 0, 255)
    cv2.circle(frame, (50, 50), 30, color, -1)
    cv2.putText(frame, f"{direction} {'GREEN' if is_green else 'RED'}", (100, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return frame

# Main loop
while True:
    frames = {}
    passed_now = 0

    for d in directions:
        ret, frame = caps[d].read()
        if not ret:
            break
        frame = cv2.resize(frame, (1280, 720))
        frame, carros[d], new_passed = process_frame(frame, subtractors[d], detecs[d], carros[d])
        frames[d] = frame

        if (signal_state == 'NS' and d in ['North', 'South']) or (signal_state == 'EW' and d in ['East', 'West']):
            passed_now += new_passed

    elapsed = time.time() - signal_start_time

    # Update last vehicle time if any vehicle passed this frame
    if passed_now > 0:
        last_vehicle_time = time.time()

    # Determine counts
    ns_count = carros['North'] + carros['South']
    ew_count = carros['East'] + carros['West']

    # Time-based or inactivity-based switching
    if elapsed >= 60 or (time.time() - last_vehicle_time >= 5):
        signal_state = 'EW' if signal_state == 'NS' else 'NS'
        signal_start_time = time.time()
        last_vehicle_time = time.time()

    # Directional priority override
    if ns_count > ew_count:
        signal_state = 'NS'
    elif ew_count > ns_count:
        signal_state = 'EW'

    # Annotate signals
    for d in directions:
        is_green = (signal_state == 'NS' and d in ['North', 'South']) or (signal_state == 'EW' and d in ['East', 'West'])
        frames[d] = annotate_signal(frames[d], is_green, d)

    top = np.hstack((frames['North'], frames['East']))
    bottom = np.hstack((frames['South'], frames['West']))
    grid = np.vstack((top, bottom))

    cv2.imshow("Smart Traffic Light Controller", grid)

    if cv2.waitKey(1) == 27:
        break

for cap in caps.values():
    cap.release()
cv2.destroyAllWindows()
