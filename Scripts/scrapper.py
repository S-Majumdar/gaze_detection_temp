import cv2
import os


def scrape(frames_dir, output_dir):
    for i in os.listdir(frames_dir):

        image = cv2.imread(os.path.join(frames_dir, i))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )

        print("Found {0} Faces!".format(len(faces)))
        os.makedirs(os.path.join(output_dir), exist_ok=True)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_color = image[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite(output_dir + "/" + str(w) +
                        str(h) + '_faces.jpg', roi_color)

        status = cv2.imwrite('faces_detected.jpg', image)
        print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
