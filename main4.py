import os
#from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask

UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
	
@app.route('/')
def upload_form():
	return render_template('upload3.html')

@app.route('/', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('upload3.html', filename=filename)

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return  send_from_directory(
        app.config['UPLOAD_FOLDER'], filename, as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)