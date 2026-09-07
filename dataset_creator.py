# dataset_creator.py

import cv2
import os


def create_dataset(user_id, camera_index=2):

    os.makedirs("dataset", exist_ok=True)

    cam = cv2.VideoCapture(camera_index)

    if not cam.isOpened():
        return False, "Could not open webcam"

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    sample_num = 0

    while True:

        ret, img = cam.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            sample_num += 1

            cv2.imwrite(
                f"dataset/User.{user_id}.{sample_num}.jpg",
                gray[y:y+h, x:x+w]
            )

        cv2.imshow(
            "Dataset Creator",
            img
        )

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        if sample_num >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()

    return True, f"{sample_num} images captured"