import cv2 as cv
from typing import List, Dict, Tuple
from math import cos, sin, pi
import numpy as np

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

    RADIUS = max(100, int(window_height * 3 / 10))
    THICKNESS = max(20, int(window_height / 10))
    CENTER = (int(window_width * 2 / 3), window_height // 2)

    """
    note on angles.
    want 0 degree to be up, 90 degree to be right, like a compass
    openCV is our regular cartesian degrees flipped over the x axis
    so the desired 0 degree is 270 degree in openCV
    Hence the (degree - 90) % 360
    """

    sector_angles = []
    for i in range(num_chords):
        start_angle = shift_degree(sector_angle/2 + i * sector_angle)
        end_angle = shift_degree(sector_angle / 2 + (i + 1) * sector_angle)
        sector_angles.append([start_angle, end_angle])

        #covers case where the angles cross 0 degrees
        if start_angle > end_angle:
            start_angle = start_angle - 360
            draw_ring_sector(
                frame,
                start_angle, #start angle
                end_angle, #end angle
                RADIUS + THICKNESS, RADIUS - THICKNESS, CENTER,
                (0, 0, 60), window_width, window_height
            )
        else:
            draw_ring_sector(
                frame,
                start_angle,  # start angle
                end_angle,  # end angle
                RADIUS + THICKNESS, RADIUS - THICKNESS, CENTER,
                (0, 0, 60), window_width, window_height
            )




    #----------------- handling text -----------------#
    text_angles = []
    for i in range(num_chords):
        text_angles.append(shift_degree(i * sector_angle))

    text_coords = []
    for i in range(num_chords):
        x = cos(text_angles[i] / 360 * 2 * pi) * RADIUS + CENTER[0]
        y = sin(text_angles[i] / 360 * 2 * pi) * RADIUS + CENTER[1]

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







def draw_ring_sector(frame, start_angle, end_angle, outer_radius, inner_radius, center, color, window_width, window_height):
    mask = np.zeros((window_height, window_width), dtype=np.uint8)

    #outer ellipse
    cv.ellipse(
        mask,
        center,
        (outer_radius, outer_radius),
        0,
        start_angle,
        end_angle,
        255,
        -1
    )

    cv.ellipse(
        mask,
        center,
        (inner_radius, inner_radius),
        0,
        start_angle - 10,
        end_angle + 10,
        0,
        -1
    )

    frame[mask==255] = color

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    outline_color = (255, 255, 255)  # White outline (BGR)
    outline_thickness = 1
    cv.drawContours(frame, contours, -1, outline_color, outline_thickness)




def shift_degree(angle: float):
    if angle < 90:
        return 270 + angle
    else:
        return angle - 90
