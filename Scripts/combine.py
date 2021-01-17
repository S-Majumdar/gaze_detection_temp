from gaze_detection_from_image_file import main
from detect_emotion import create_df
import os
import sys
from flask import Flask, render_template


UPLOAD_FOLDER = os.path.join("static", "images")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/combined')
def combine():
	#os.rmdir("videos")
	emotion_detect = create_df()
	gaze_prediction = main()
	return render_template("plot.html", user_image=os.path.join(app.config['UPLOAD_FOLDER'], 'heatmap.jpg'), 
		user_image_1=os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
