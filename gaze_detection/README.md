# gaze_detection 

By pussydestroyer_69_420 a.k.a Pandaboi3010 a.k.a AhsokaTano332nd a.k.a ur_mom_gay_for_my_dick_69
## How to run
Run code using 
`python gaze_detection_from_image_file.py`
Directory for video frames is hardcoded to `/vids/frames`

Output is sent to flask application at
`http://localhost:5000/gaze_detection`
Additionally, a heatmap of gaze points is saved to the `/images` directory as `heatmap.jpg`
The picture is overwritten everytime the script runs

## requirements.txt
All dependencies recorded here

##TODO
- Add `render_template` for flask output with heatmap and prediction percentage shown
- Add funtionality for choosing different video directory from commannd line
- Add functionality for varible focal point and predict using that list of focal points
