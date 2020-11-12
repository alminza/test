# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from PIL import Image
import os, sys
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for



UPLOAD_FOLDER = '/home/malcor'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return 

def open_and_extract(input):
    im = Image.open(input)
    im.show(input)
    print(im.format, im.size, im.mode)
    print(id(im))

def minaturization():
    
    size = (128, 128)

    for infile in sys.argv[1:]:
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                with Image.open(infile) as im:
                    im.thumbnail(size)
                    im.save(outfile, "JPEG")
                    print(outfile)
            except OSError:
                print("cannot create thumbnail for", infile)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run()