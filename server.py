import os
import ntpath
from os.path import join, dirname, realpath
from flask import Flask, flash, request, redirect, url_for, send_from_directory, send_file
from flask import jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads/images')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


import cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name = 'dggbuxa59',  
  api_key = '651855936159331',  
  api_secret = 'YZcmgha2qUntVE_QrxeCThMLJEM'  
)

def upload_diary(filename):
  OUTPUT_FOLDER = os.path.join(APP_ROOT, 'output/colorize/')
  os.chdir(OUTPUT_FOLDER)
  respone = cloudinary.uploader.upload(filename, folder = "colorize")
  return respone['url']



@app.route('/', methods=['GET', 'POST'])
def welcome():
  return "Hello World"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(
              success=False,
              message="No file",
            )
        file = request.files['file']
        if file.filename == '':
              return jsonify(
              success=False,
              message="File name is blank",
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #colorize
            command = "python3 colorization/demo_release.py -i " + UPLOAD_FOLDER + "/" + filename
            os.system(command)
            out_img_eccv16_name = str(filename + "_eccv16.png")
            out_img_siggraph17_name = str(filename + "_siggraph17.png")
            url1 = upload_diary(out_img_eccv16_name)
            url2 = upload_diary(out_img_siggraph17_name)
            return jsonify(
              success=True,
              message="File name is uploaded",
              fileName=file.filename,
              path=UPLOAD_FOLDER,
              script=command,
              url1=url1,
              url2=url2
            )


    return "This is GET method"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)


