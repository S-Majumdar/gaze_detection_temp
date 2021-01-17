import numpy as np
import sklearn
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from flask import Flask, render_template
import extract_frames
import scrapper
import time

# create command to execute conversion script.
# ffmpeg - i .\nihir_faces.webm .\nihir_faces.mp4 to convert webm to mp4
from flask import Flask

UPLOAD_FOLDER = os.path.join("static", "images")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("static", "images")


def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    #likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE','LIKELY', 'VERY_LIKELY')
    likelihood_name = (0, 1, 2, 3, 4, 5)
#     print('Faces:')
    dict_face = {'anger': "", 'joy': '', 'surprise': '', 'sorrow': ''}
    for face in faces:
        #         print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #         print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #         print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        #         print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        dict_face['anger'] = likelihood_name[face.anger_likelihood]
        dict_face['joy'] = likelihood_name[face.joy_likelihood]
        dict_face['surprise'] = likelihood_name[face.surprise_likelihood]
        dict_face['sorrow'] = likelihood_name[face.sorrow_likelihood]

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                       for vertex in face.bounding_poly.vertices])

#         print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return dict_face


def emotion_percentage(emotion_df):
    dict_emotion = {}
    for i in list(emotion_df.columns):
        count_2 = 0
        for j in list(emotion_df[i]):
            if float(j) > 2.0:
                count_2 += 1
        dict_emotion[i] = (count_2/len(emotion_df[[i]])) * 100
    return dict_emotion


# function to parse and create the dataframe
# def create_df(img_directory):
#     df = pd.DataFrame()
#     for i in os.listdir(img_directory):
#         temp_dict = detect_faces(os.path.join(img_directory, i))
#         df = df.append(temp_dict, ignore_index=True)
#     df

# create some sort of graph so that the doctor can see emotions,
# I also think we need to display the stimuli that was used, lets see how that will work.
# probably make a django repository for the app and see how it shapes out.

def create_df():
    frames_dir = 'vid_frames'
    output_dir = 'vid_output'
    extract_frames.video_to_frames(
        sys.argv[1], frames_dir, overwrite=False, every=5)

    scrapper.scrape(frames_dir, output_dir)
    print(output_dir)
    # extract frames from video
    df = pd.DataFrame()
    for i in os.listdir(output_dir):
        temp_dict = detect_faces(os.path.join(output_dir, i))
        if temp_dict['anger'] == '' or temp_dict['joy'] == '' or temp_dict['surprise'] == '' or temp_dict['sorrow'] == '':
            continue
        else:
            print(temp_dict)
            df = df.append(temp_dict, ignore_index=True)
    dict_plot = emotion_percentage(df)
    create_plot(dict_plot)
    print(dict_plot)
    time.sleep(20)
    return ("success")
    # return render_template("plot.html", user_image=os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png'))


def create_plot(plot_dict):
    plt.bar(range(len(plot_dict)), list(plot_dict.values()), align='center')
    plt.xticks(range(len(plot_dict)), list(plot_dict.keys()))
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png'))


def predict_autism(predict_dict):
    count_emotion = 0
    for i in predict_dict.keys():
        if float(predict_dict[i]) > 20.0:
            count_emotion += 1


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
