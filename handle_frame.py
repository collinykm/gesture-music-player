import cv2 as cv
from typing import List, Dict, Tuple
from math import cos, sin, pi

def handle_frame(frame, latest_processed_data: Dict, chords):
    if latest_processed_data["gesture"] is not None:
        cv.putText(
            frame,
            f"{latest_processed_data["gesture"]}: {str(latest_processed_data["confidence"])}",
            (latest_processed_data["window_width"] - 300, latest_processed_data["window_height"] - 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255))


        cv.circle(frame, (latest_processed_data["index_tip_x"], latest_processed_data["index_tip_y"]), 20, (0, 0, 255), 5)
        cv.circle(frame, (latest_processed_data["index_tip_x"], latest_processed_data["index_tip_y"]), 10, (0, 0, 255), 3)

    draw_chord_circle(frame, chords, latest_processed_data["window_width"], latest_processed_data["window_height"])

    cv.imshow('Gesture Player', frame)


def draw_chord_circle(frame, chords: List[str], window_width, window_height):

    FONT_FACE = cv.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 1.5
    FONT_THICKNESS = 5
    FONT_COLOR = (0, 0, 0)


    num_chords = len(chords)
    sector_angle = 360.0 / num_chords

    radius = max(100, int(window_height * 3 / 10))
    thickness = max(20, int(window_height / 10))
    center = (int(window_width * 2 / 3), window_height // 2)

    """
    note on angles.
    want 0 degree to be up, 90 degree to be right, like a compass
    openCV is our regular cartesian degrees flipped over the x axis
    so the desired 0 degree is 270 degree in openCV
    Hence the (degree - 90) % 360
    """

    start_end_sector_angles = []
    for i in range(num_chords):
        start_end_sector_angles.append([shift_degree(sector_angle/2 + i * sector_angle), shift_degree(sector_angle/2 + (i + 1) * sector_angle)])

    text_angles = []
    for i in range(num_chords):
        text_angles.append(shift_degree(i * sector_angle))

    text_coords = []
    for i in range(num_chords):
        x = cos(text_angles[i] / 360 * 2 * pi) * radius + center[0]
        y = sin(text_angles[i] / 360 * 2 * pi) * radius + center[1]

        #calculate the offset needed to center text
        textSize = cv.getTextSize(chords[i], FONT_FACE,FONT_SCALE,FONT_THICKNESS)[0]
        offset_x = textSize[0]/2
        offset_y = textSize[1]/2

        cv.putText(
            frame,
            chords[i],
            (int(x - offset_x), int(y + offset_y)),
            FONT_FACE,
            FONT_SCALE,
            FONT_COLOR,
            FONT_THICKNESS,
        )



    cv.circle(frame, center, radius + thickness, (0, 0, 0), 5)
    cv.circle(frame, center, radius - thickness, (0, 0, 0), 5)




def shift_degree(angle: float):
    if angle < 90:
        return 270 + angle
    else:
        return angle - 90
