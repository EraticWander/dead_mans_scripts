from flask import Flask, render_template, request, send_file, after_this_request
import os
from imageencryptor import ImageEncryptor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def encode_image(image_path, message, passphrase):
    print (image_path)
    print (message)
    image_encryptor = ImageEncryptor(passphrase)
    encrypted_image_path = image_encryptor.encrypt_message(image = image_path, message=message)
    return encrypted_image_path

def decode_image(image_path, passphrase):
    image_decryptor = ImageEncryptor(passphrase)
    decrypted_message = image_decryptor.decrypt_message(image_path)
    return decrypted_message

@app.route('/', methods=['GET', 'POST'])
def encrypt_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        
        file = request.files['file']
        passphrase = request.form['passphrase']
        message = request.form['message']
        
        if file.filename == '':
            return 'No selected file'
            
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            output = encode_image(image_path=file_path, message=message, passphrase=passphrase)
            if output and os.path.exists(output):
                @after_this_request
                def cleanup_files(response):
                    try:
                        # Delete the original uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        # Delete the encrypted image file
                        if os.path.exists(output):
                            os.remove(output)
                    except Exception as e:
                        print(f"Error during cleanup: {e}")
                    return response
            # Send the encrypted image back to the user for download
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=filename + '_encrypted.png',
                    mimetype='image/png'
                )
            else:
                return 'Error processing the image'
        
    return render_template('upload.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']
        passphrase = request.form['passphrase']

        if file.filename == '':
            return 'No selected file'

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            decrypted_message = decode_image(image_path=file_path, passphrase=passphrase)
            if file_path:
                @after_this_request
                def cleanup_files(response):
                    try:
                        # Delete the original uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error during cleanup: {e}")
                    return response

            if decrypted_message:
                return render_template('decrypt.html', message=decrypted_message)
            else:
                return 'Error decrypting the image'

    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
