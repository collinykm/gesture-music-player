import cv2 as cv
import mediapipe as mp

def process_data(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int, latest_processed_data):
    window_width, window_height = cv.getWindowImageRect("Gesture Player")[2:]

    latest_processed_data["window_width"] = window_width
    latest_processed_data["window_height"] = window_height
    print(result.gestures)
    if result.gestures != []: #essentially saying it still detects a hand
        #print('gesture recognition result: {}'.format(result.gestures[0][0].category_name))

        latest_processed_data["confidence"] = round(result.gestures[0][0].score, 2)

        latest_processed_data["index_tip_x"] = int(result.hand_landmarks[0][8].x * window_width)
        latest_processed_data["index_tip_y"] = int(result.hand_landmarks[0][8].y * window_height)
        latest_processed_data["gesture"] = result.gestures[0][0].category_name
    else: #if there's straight up no hand
        latest_processed_data["gesture"] = None
        latest_processed_data["index_tip_x"] = None
        latest_processed_data["index_tip_y"] = None