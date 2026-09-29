import cv2 as cv

def handle_frame(frame, latest_processed_data):
    print(latest_processed_data)
    if latest_processed_data["gesture"] != None:
        cv.putText(
            frame,
            f"{latest_processed_data["gesture"]}: {str(latest_processed_data["confidence"])}",
            (latest_processed_data["window_width"] - 300, latest_processed_data["window_height"] - 100),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255))


        cv.circle(frame, (latest_processed_data["index_tip_x"], latest_processed_data["index_tip_y"]), 20, (0, 0, 255), 5)
        cv.circle(frame, (latest_processed_data["index_tip_x"], latest_processed_data["index_tip_y"]), 10, (0, 0, 255), 3)

    cv.imshow('Gesture Player', frame)