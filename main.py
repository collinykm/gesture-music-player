import functools
import time
import cv2 as cv
import mediapipe as mp
from process_data import process_data
from handle_frame import handle_frame
# Open the default camera
cam = cv.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(
cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(
cv.CAP_PROP_FRAME_HEIGHT))



BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizer
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the live stream mode:
latest_processed_data = {
    "gesture": None,
    "confidence": None,
    "index_tip_x": None,
    "index_tip_y": None,
    "window_width": None,
    "window_height": None,
}

chords = ["A-", "D7", "Gmaj7", "Cmaj7", "F#6", "B7", "E-"]

callback = functools.partial(process_data, latest_processed_data=latest_processed_data)

options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path='gesture_recognizer.task',
    ),
    num_hands=2,
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=callback)

with GestureRecognizer.create_from_options(options) as recognizer:


    # setting up webcam
    while True:
        ret, frame = cam.read()
        t = int(time.time() * 1000)
        mp_image = None

        if ret:
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            recognizer.recognize_async(mp_image, t)





            # Display the captured frame
            handle_frame(frame, latest_processed_data)





        # Press 'q' to exit the loop
        if cv.waitKey(1) & 0xFF == 27:
            break



cam.release()
cv.destroyAllWindows()