import cv2
from gaze_detector import extract_features_and_detect_gazes

img = cv2.imread('notebooks/photos/WIN_20210113_20_03_29_Pro.JPG')

outputs = extract_features_and_detect_gazes(img)

print(outputs)
