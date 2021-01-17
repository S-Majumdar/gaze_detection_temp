from os import listdir
from os.path import isfile, join
import numpy
import cv2
from gaze_detector import extract_features_and_detect_gazes
from flask import Flask, render_template
import pandas as pd
import os

###################################################################################################################
# Precondition  - Video frames are taken every 0.5 second and placed in frames directory. Resolution is 1280x720
# Postcondition - Returns a list that show the euclidean distance from focus point (image centre - default).
#                     Result values are in pixels
# Summary       - Results from model are scaled up for a 13 inch screen (Scaling was trail and error; Can be improved)
#                     Dont really know how to explain the variables for scaling.
# TO_DO         - Calculate std deviation of distance from focal point.
#                     Add functionality to change focal point or have focal region.
#                     Verify distance calculation. Math looks fine but the numbers dont seem accurate.
#                     Make prediction weighted with more variables
#                     Display output in html file with prediction and simple gaze heatmap
###################################################################################################################
UPLOAD_FOLDER = os.path.join("static", "images")

# app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



def main():
    mypath = 'vids/frames/'
    photos_file = [i for i in listdir(mypath) if isfile(join(mypath, i))]
    images = numpy.empty(len(photos_file), dtype=object)
    for n in range(0, len(photos_file)):
        images[n] = cv2.imread(join(mypath, photos_file[n]))

    outputs = []
    for i in range(len(images)):
        outputs.append(extract_features_and_detect_gazes(images[i]))

    # print(outputs)

    # scale up gaze estimatation for 15 or 13 inch screen
    # 3810 for 15 inch screen or 3302 for 13 inch screen
    screen_size = 3302
    screen_width = screen_size
    screen_height = screen_size
    camera_pixels_from_l = screen_width / 1.5
    camera_pixels_from_top = screen_height / 1.5
    # pixels_per_cm          = screen_size / 25.0

    # gaze estimate drawn on top of original
    window_width = 1280
    window_height = 720
    window_height_cm = 15
    camera_h_from_screen_top = 5

    pixels_per_cm = window_height * 1. / window_height_cm

    camera_pixels_from_l = window_width / 2
    camera_pixels_from_top = camera_h_from_screen_top * pixels_per_cm
    # print(camera_pixels_from_top)

    x_translation_from_camera_c = camera_pixels_from_l
    y_translation_from_camera_c = camera_pixels_from_top

    print(pixels_per_cm, x_translation_from_camera_c,
          y_translation_from_camera_c)
    print(outputs)

    pos_in_pixel = []
    for output in outputs:
        if len(output) == 1:
            if isinstance(output[0], numpy.ndarray):
                screen_x = output[0][0] * pixels_per_cm + \
                    x_translation_from_camera_c
                screen_y = -output[0][1] * pixels_per_cm + \
                    y_translation_from_camera_c

                print("in px:", round(screen_x), round(screen_y))
                pos_in_pixel.append([round(screen_x), round(screen_y)])
    print(pos_in_pixel)

    # default - centre of 1280x720 window
    focal_point = [640, 360]

    results = []
    for i in range(len(pos_in_pixel)):
        a = numpy.array(focal_point)
        b = numpy.array(pos_in_pixel[i])
        distance = numpy.linalg.norm(b-a)
        results.append(int(round(distance)))
    print(results)
    final = simple_predict_adhd(results)
    create_heatmap(pos_in_pixel, focal_point,results)

    print("\n Chance of Autism/ADHD based on gaze estimates: %d%%\n" % final)
    # return("Chance of Autism/ADHD based on gaze estimates: %d%%" % final)
    # return render_template("plot.html", user_image=os.path.join(UPLOAD_FOLDER, 'heatmap.jpg'), 
    #     estimate = "Chance of Autism/ADHD based on gaze estimates: %d%%" % final)
    return(final)


# Simple prediction: No weighted ranks
def simple_predict_adhd(results):
    df = pd.DataFrame(results, columns=["Distance"])
    mean = int(df.mean())
    std = int(df.std())
    mean_per = 0
    std_per = 0

    # some stupid temporary hardcoded thresholds
    if mean <= 350:
        mean_per = 0.33
    if mean > 350 & mean <= 400:
        mean_per = 0.5
    if mean > 400 & mean <= 450:
        mean_per = 0.67
    if mean > 450:
        mean_per = 0.93

    if std <= 350:
        std_per = 0.33
    if std > 350 & std <= 400:
        std_per = 0.5
    if std > 400 & std <= 450:
        std_per = 0.67
    if std > 450:
        std_per = 0.93

    # Weightage: Mean distance - 60%, Stnd Dev - 40%
    final_predict = ((mean_per*0.6) + (std_per*0.4))*100

    # will add html page which gives weighted prediction and simple heatmap
    return (final_predict)


def create_heatmap(pos_in_pixel, focal_point,results):
    image   = cv2.imread(os.path.join(app.config["UPLOAD_FOLDER"], "black.jpg"))
    predict = simple_predict_adhd(results)
    #cv2.namedWindow("image frame", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("image frame", 1280, 720)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image,"Chance of Autism/ADHD based on gaze estimates: %d%%" %predict, (0,30),font,1,(255,255,255),2)


    # draw circles for gaze estimate location
    for i in range(len(pos_in_pixel)):
        cv2.circle(image, (int(round(pos_in_pixel[i][0])), int(
            round(pos_in_pixel[i][1]))), 20, (0, 0, 255), 2)
    # draw circle for focal point
    cv2.circle(image, (focal_point[0], focal_point[1]), 20, (255, 0, 0), 2)
    cv2.imwrite(os.path.join(UPLOAD_FOLDER, "heatmap.jpg"), image)

    print("heatmap created")



# def rank_flag_frames(results):
#     flag_frame_ranked = [[0],[0],[0]]
#     frame_count = len(results)
#     for i in range(frame_count):
#         if results[i] > 350 & results[i] <= 400:
#             flag_frame_ranked[0] += 1
#         if results[i] >400 & results[i] <= 450:
#             flag_frame_ranked[1] += 1
#         if results[i] > 450:
#             flag_frame_ranked[2] += 1

#     return flag_frame_ranked


# focal_point = (640,360)
# results = []
# for i in range(len(pos_in_pixel)):
#     a        = numpy.ndarray(focal_point)
#     b        = numpy.ndarray(pos_in_pixel[i])
#     distance = numpy.linalg.norm(a-b)
#     results.append(int(round(distance)))

# print(results)


##########################################################################################################
# Code to display a simple heat map of all gaze points during the video. Can be used for presentation.
##########################################################################################################
# image = cv2.imread('images/black.jpg')
# cv2.namedWindow("image frame", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("image frame", 1280, 720)
# for i in range(len(pos_in_pixel)):
#     cv2.circle(image, (int(round(pos_in_pixel[i][0])),int(round(pos_in_pixel[i][1]))), 20, (0, 0, 255), 2)
# cv2.circle(image, (640,360), 20, (255, 0, 0), 2)
# cv2.imshow("image frame",image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


##########################################################################################################
# Abosulte dog shit useless part of the code. only for debugging. do not look here. HORN OK TATA.
##########################################################################################################
# for output in outputs:
#     screen_x = output[0] * pixels_per_cm + camera_pixels_from_l
#     screen_y = -output[1] * pixels_per_cm + camera_pixels_from_top

#     screen_x = output[0] * pixels_per_cm + x_translation_from_camera_c
#     screen_y = -output[1] * pixels_per_cm + y_translation_from_camera_c

# cv2.namedWindow("image frame", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("image frame", 1280, 720)
# image = cv2.flip(image,1)
# cv2.circle(image, (int(round(screen_x)),int(round(screen_y))), 20, (0, 0, 255), 2)
# cv2.imshow("image frame",image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Code to run gaze_estimation on multiple photos
# mypath='images/'
# photos_file = [ i for i in listdir(mypath) if isfile(join(mypath,i)) ]
# images = numpy.empty(len(photos_file), dtype=object)
# for n in range(0, len(photos_file)):
#   images[n] = cv2.imread( join(mypath,photos_file[n]) )

# outputs = []
# for i in range(len(images)):
#     outputs.append(extract_features_and_detect_gazes(images[i]))

# for i in range(len(outputs)):
#     print(" shift ")
#     for j in range(len(outputs[i])):
#         print(type(outputs[i][j]))

# img = cv2.imread('notebooks/photos/WIN_20210113_20_03_29_Pro.JPG')
