from features import extract_image_features
from gaze import test_faces

#################################################################
# Precondition  - image file from cv2.imread
#                     File combines both gaze.py and features.py
# Postcondition - if face detected, nd.array with x and y coords; else returns NoneType
# Summary       - Gets facial features from features.py and runs feautrues through the itracker model
#################################################################

def extract_features_and_detect_gazes(img):
    img, faces, face_features = extract_image_features(img)
    return test_faces(img, faces, face_features)
