from flask import Flask, request, Response
import subprocess
import shutil
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert/form-data', methods=['POST'])
def convert_ogg_to_wav():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']

    if not file.filename.endswith('.ogg'):
        return "Invalid file format. Only .ogg files are supported", 400

    unique_folder_name = str(uuid.uuid4())
    uuid_folder_path = os.path.join(UPLOAD_FOLDER, unique_folder_name)
    os.makedirs(uuid_folder_path, exist_ok=True)

    filename = str(file.filename)
    input_path = os.path.join(uuid_folder_path, filename)
    output_path = os.path.join(uuid_folder_path, filename.replace('.ogg', '.wav'))
    file.save(input_path)

    try:
        subprocess.run(['ffmpeg', '-i', input_path, output_path], check=True)
        with open(output_path, 'rb') as wav_file:
            wav_data = wav_file.read()
        return Response(wav_data, mimetype='audio/wav', headers={'Content-Disposition': f'attachment; filename={filename.replace(".ogg", ".wav")}'})
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}", 500
    finally:
        shutil.rmtree(uuid_folder_path)

@app.route('/convert/bytes', methods=['POST'])
def convert_ogg_bytes_to_wav():
    if not request.data:
        return "No data provided", 400

    unique_folder_name = str(uuid.uuid4())
    uuid_folder_path = os.path.join(UPLOAD_FOLDER, unique_folder_name)
    os.makedirs(uuid_folder_path, exist_ok=True)

    input_path = os.path.join(uuid_folder_path, 'input.ogg')
    output_path = os.path.join(uuid_folder_path, 'output.wav')

    try:
        with open(input_path, 'wb') as f:
            f.write(request.data)

        subprocess.run(['ffmpeg', '-i', input_path, output_path], check=True)

        with open(output_path, 'rb') as wav_file:
            wav_data = wav_file.read()

        return Response(wav_data, mimetype='audio/wav')
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}", 500
    finally:
        shutil.rmtree(uuid_folder_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)