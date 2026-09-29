import cv2 as cv
import mediapipe as mp
from config import latest_processed_data
from math import sqrt, atan2, pi
from typing import Tuple

def process_recognizer_data(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):

    window_width = latest_processed_data["window_width"]
    window_height = latest_processed_data["window_height"]
    try:

        if result.gestures != []: #essentially saying it still detects a hand
            #print('gesture recognition result: {}'.format(result.gestures[0][0].category_name))
            window_width, window_height = cv.getWindowImageRect("Gesture Player")[2:]

            latest_processed_data["confidence"] = round(result.gestures[0][0].score, 2)
            latest_processed_data["index_tip_x"] = int(result.hand_landmarks[0][8].x * window_width)
            latest_processed_data["index_tip_y"] = int(result.hand_landmarks[0][8].y * window_height)
            latest_processed_data["gesture"] = result.gestures[0][0].category_name
        else: #if there's straight up no hand
            latest_processed_data["gesture"] = None
            latest_processed_data["index_tip_x"] = None
            latest_processed_data["index_tip_y"] = None
    except:
        print("widow not yet initialized")


def finger_in_ring_sector(center: Tuple[int, int], outer_radius, inner_radius, start_angle, end_angle):
    index_x: float = latest_processed_data["index_tip_x"]
    index_y: float = latest_processed_data["index_tip_y"]
    if index_x is None:
        return False

    x = index_x - center[0]
    y = index_y - center[1]

    radius = sqrt(pow(x, 2) + pow(y, 2))
    angle = atan2(y, x)

    #parsing angles
    #converting atan2
    if y < 0:
        angle += 2 * pi
    angle = angle / pi * 180

    angle_correct_in_edge_case = False

    if start_angle > end_angle and (angle >= start_angle or angle <= end_angle): #to handle the case if start angle was like 330 and end angle was 30
        angle_correct_in_edge_case = True


    print(f"x: {x}, y: {y}, radius: {radius}, angle: {angle}")

    if inner_radius <= radius <= outer_radius and (angle_correct_in_edge_case or start_angle <= angle <= end_angle) and latest_processed_data["gesture"] == "Open_Palm":
        return True
    else:
        return False


