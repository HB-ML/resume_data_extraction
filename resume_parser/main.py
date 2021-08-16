import json
import os
import requests



from flask import Flask, request, jsonify, render_template, make_response
from werkzeug.utils import secure_filename

from resume_parser.resume_parser import ResumeParser

app = Flask(__name__)
app.secret_key = '\xd9\xa5\xf9Y/\xb819]\xad\xecbE\xfc\x89\xe2\xa1\x97\xc55\xab\xc5\xa8o\xb2\xf1\xfdbA\xc1'

UPLOAD_FOLDER = \
    os.path.dirname(os.path.realpath(__file__)) + '/mediafiles/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'doc', 'pdf', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_resume', methods=['POST'])
def upload_file():
    # try:
        if request.method == 'POST':
            file = request.files['resume']
            filename = file.filename
            if filename == '':
                return jsonify({
                    'error': 'No selected file',
                    'data': {}}), 400
            if filename and allowed_file(filename):
                file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], secure_filename(filename))

                file.save(file_path)

                # extracting resume entities
                parser = ResumeParser(file_path)
                data = parser.get_extracted_data()


                os.remove(file_path)

                return make_response(
                    ({'error': False,
                      "data": data},
                     '200'))

            else:
                return jsonify({
                    'error': 'File format not supported. \
                        Please upload .pdf, .dox or .docx file.',
                    'data': {}}), 400
        return jsonify({
            'error': 'Request Method is not supported, \
                please use request method as POST',
            'data': {}}), 405

    # except Exception as err:
    #     return jsonify({
    #         'error': 'Request Method is not supported, \
    #             please use request method as POST',
    #         'data': {}}), 405
    #

if __name__ == '__main__':
    app.run(port=5050, host="0.0.0.0")
