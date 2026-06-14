import cv2
import numpy as np

# ------------------------------------
# Slot Regions
# ------------------------------------

A_REGION = (175, 335, 230, 385)
B_REGION = (290, 335, 345, 385)
C_REGION = (405, 335, 460, 385)

# ------------------------------------
# Helper Functions
# ------------------------------------

def point_in_region(cx, cy, region):

    x1, y1, x2, y2 = region

    return x1 <= cx <= x2 and y1 <= cy <= y2


def get_slot(cx, cy):

    if point_in_region(cx, cy, A_REGION):
        return "A"

    if point_in_region(cx, cy, B_REGION):
        return "B"

    if point_in_region(cx, cy, C_REGION):
        return "C"

    return None


# ------------------------------------
# Main Function
# ------------------------------------

def get_scene():

    cap = cv2.VideoCapture(0)

    import time

    time.sleep(2)

    for _ in range(30):
        ret, frame = cap.read()

    if not ret:

        cap.release()

        return None

    frame = cv2.flip(frame, -1)
#    cv2.imwrite("debug.jpg", frame)
#    print("Saved debug.jpg")

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    scene = {

        "slots": {
            "A": None,
            "B": None,
            "C": None
        },

        "bins": {
            "LEFT": None,
            "RIGHT": None
        }
    }

    # ==================================================
    # GREEN DETECTION
    # ==================================================

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    contours, _ = cv2.findContours(
        green_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        cx = x + w // 2
        cy = y + h // 2

        aspect_ratio = w / h

        # GREEN BIN

        if (
            area > 5000
            and 0.7 < aspect_ratio < 1.3
            and (cx < 150 or cx > 500)
        ):

            if cx < frame.shape[1] // 2:

                scene["bins"]["LEFT"] = "green_bin"

            else:

                scene["bins"]["RIGHT"] = "green_bin"

        # GREEN CUBE

        else:

            slot = get_slot(cx, cy)

            if slot:

                scene["slots"][slot] = "cube_green"

    # ==================================================
    # RED DETECTION
    # ==================================================

    lower_red1 = np.array([0, 80, 80])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 80, 80])
    upper_red2 = np.array([180, 255, 255])

    red_mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    red_mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    red_mask = red_mask1 + red_mask2

    contours, _ = cv2.findContours(
        red_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        cx = x + w // 2
        cy = y + h // 2

        aspect_ratio = w / h

        # RED BIN

        if (
            area > 5000
            and 0.7 < aspect_ratio < 1.3
            and (cx < 150 or cx > 500)
        ):

            if cx < frame.shape[1] // 2:

                scene["bins"]["LEFT"] = "red_bin"

            else:

                scene["bins"]["RIGHT"] = "red_bin"

        # RED CUBE

        else:

            slot = get_slot(cx, cy)

            if slot:

                scene["slots"][slot] = "cube_red"

    cap.release()

    return scene
