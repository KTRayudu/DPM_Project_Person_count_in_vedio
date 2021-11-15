from bokeh.resources import INLINE
from flask import Flask, render_template, redirect, url_for, session, request
import dpm_object_detection_video as obj_det
from werkzeug.utils import secure_filename
import os
import Live_graph_creator as graph_creator
app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

@app.route('/', methods=["GET"]) # Only get method is allowed for input page
def input_page():
    #video_photo = os.path.join(app.config['UPLOAD_FOLDER'],'video_analysis.jpeg')
    return render_template('input_page.html',js_resources=INLINE.render_js(),
    css_resources=INLINE.render_css()).encode(encoding='UTF-8')

@app.route('/', methods=["POST"])
def action(): # currently independent of user uploaded video
    file = request.files["video"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    model, classLabels = obj_det.load_pretrained_model() # Load a pre-trained model
    obj_det.setInputParams(model=model) # Set input parameters to the model
    
    video_src = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    refresh_rate = 5 # after every 5 frame update the Processed_frame, script and div
    i = 0
    FRAME_LIMIT = 216000 # a 60 fps video for 30 min can be handled
    Processed_frame, script, div = obj_det.real_time_detection(model=model, classLabels=classLabels
                    , video_src=video_src,start_frame= i*refresh_rate, stop_after=refresh_rate) # in video source give path of user uploaded video.
    
		
	
    
    return render_template('output_page.html', video_frame=Processed_frame, 
        plot_script=script, plot_div=div, js_resources = INLINE.render_js(), css_resources=INLINE.render_css(),filename=filename
        ).encode(encoding='UTF-8')

@app.route('/<filename>')
def display_video(filename):
	print('display_video filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)