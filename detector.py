import cv2
import time

from telegram_utils import (
    send_telegram_photo,
    send_telegram_video
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    "face-trainer.yml"
)

faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

RAMYA_ID = 1

last_alert = 0


def record_video(cap):

    video_path = (
        f"recordings/intruder_{int(time.time())}.avi"
    )

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(
        video_path,
        fourcc,
        20.0,
        (640, 480)
    )

    start_time = time.time()

    while time.time() - start_time < 8:

        ret, frame = cap.read()

        if not ret:
            break

        out.write(frame)

    out.release()

    return video_path


def run_detector(frame, cap):

    global last_alert

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = faceCascade.detectMultiScale(
        gray,
        1.2,
        5
    )

    for (x, y, w, h) in faces:

        Id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        if confidence < 70 and Id == RAMYA_ID:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                "RAMYA",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

        else:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,0,255),
                3
            )

            cv2.putText(
                frame,
                "UNKNOWN",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )

            current_time = time.time()

            if current_time - last_alert > 8:

                snapshot_path = (
                    f"snapshots/unknown_{int(time.time())}.jpg"
                )

                cv2.imwrite(
                    snapshot_path,
                    frame
                )

                try:

                    send_telegram_photo(
                        snapshot_path
                    )

                    video_path = record_video(
                        cap
                    )

                    send_telegram_video(
                        video_path
                    )

                except Exception as e:

                    print(e)

                last_alert = current_time

    return frame