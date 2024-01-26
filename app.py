import os
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from CalculatorScript import main as process_file  

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = '/path/to/uploaded/files'
app.config['OUTPUT_FOLDER'] = '/path/to/output/files'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the file from the form
        file = request.files['file']
        
        if file:
            # Secure the filename and save the file to the UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Process the file
            output_filename = process_file(input_path)  # Your process_file function should return the output filename
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Send the processed file for download
            return send_file(output_path, as_attachment=True)
    
    return "There was an error uploading the file.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
