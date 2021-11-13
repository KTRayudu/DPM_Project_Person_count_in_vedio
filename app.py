from bokeh.resources import INLINE
from flask import Flask, render_template, redirect, url_for, session, request
import object_detection_video as obj_det
import os
import Live_graph_creator as graph_creator
app = Flask(__name__)


vidFolder = os.path.join('static','vid')
app.config['UPLOAD_FOLDER'] = vidFolder

@app.route('/', methods=["GET"]) # Only get method is allowed for input page
def input_page():
    video_photo = os.path.join(app.config['UPLOAD_FOLDER'],'video_analysis.jpeg')
    return render_template('input_page.html', img = video_photo,js_resources=INLINE.render_js(),
    css_resources=INLINE.render_css()).encode(encoding='UTF-8')

@app.route('/action_page', methods=["POST"])
def action(): # currently independent of user uploaded video
    model, classLabels = obj_det.load_pretrained_model() # Load a pre-trained model
    obj_det.setInputParams(model=model) # Set input parameters to the model
    video_src = 'videos/videoplayback.mp4'

    refresh_rate = 5 # after every 5 frame update the Processed_frame, script and div
    i = 0
    FRAME_LIMIT = 216000 # a 60 fps video for 30 min can be handled
    Processed_frame, script, div = obj_det.real_time_detection(model=model, classLabels=classLabels
                    , video_src=video_src,start_frame= i*refresh_rate, stop_after=refresh_rate) # in video source give path of user uploaded video. 
    
    return render_template('output_page.html', video_frame=Processed_frame, 
        plot_script=script, plot_div=div, js_resources = INLINE.render_js(), css_resources=INLINE.render_css(),
        ).encode(encoding='UTF-8')


if __name__ == "__main__":
    app.run(debug=True)
