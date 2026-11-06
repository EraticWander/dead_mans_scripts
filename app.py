from flask import Flask, render_template, request, send_file, after_this_request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from imageencryptor import ImageEncryptor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def encode_image(image_path, message, passphrase):
    image_encryptor = ImageEncryptor(passphrase)
    encrypted_image_path = image_encryptor.encrypt_message(image=image_path, message=message)
    return encrypted_image_path


def decode_image(image_path, passphrase):
    image_decryptor = ImageEncryptor(passphrase)
    decrypted_message = image_decryptor.decrypt_message(image_path)
    return decrypted_message


def build_download_name(original_filename: str) -> str:
    """Return a clean `<name>_encrypted.png` download filename without duplicating suffixes."""
    safe_name = secure_filename(original_filename) or "image"
    stem, _ = os.path.splitext(safe_name)
    if not stem.endswith("_encrypted"):
        stem = f"{stem}_encrypted"
    return f"{stem}.png"


def save_temp_upload(file_storage) -> str:
    """Save an uploaded file to UPLOAD_FOLDER with a unique filename to avoid collisions."""
    safe_name = secure_filename(file_storage.filename) or "upload.png"
    _, ext = os.path.splitext(safe_name)
    unique_name = f"{uuid.uuid4().hex}{ext or '.png'}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file_storage.save(file_path)
    return file_path


def remove_file_safely(path: str):
    """Delete a file if it exists, logging any cleanup error."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error during cleanup of {path}: {e}")


@app.route('/', methods=['GET', 'POST'])
def encrypt_image():
    if request.method == 'POST':
        return api_encrypt()
    return render_template('upload.html')


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_image():
    if request.method == 'POST':
        return api_decrypt()
    return redirect(url_for('encrypt_image'))


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': 'No image file was uploaded.'}), 400

    file = request.files['file']
    passphrase = request.form.get('passphrase', '').strip()

    if not file or file.filename == '':
        return jsonify({'ok': False, 'error': 'Please select an image file to decode.'}), 400

    if not passphrase:
        return jsonify({'ok': False, 'error': 'Please enter the secret passphrase.'}), 400

    file_path = save_temp_upload(file)
    try:
        decrypted_message = decode_image(image_path=file_path, passphrase=passphrase)
    finally:
        # Always remove the temporary uploaded image immediately after decoding
        remove_file_safely(file_path)

    if decrypted_message is not None:
        return jsonify({
            'ok': True,
            'message': decrypted_message,
            'filename': file.filename
        })
    else:
        return jsonify({
            'ok': False,
            'error': 'Could not decode a hidden message. Please verify your passphrase and make sure this PNG contains an encoded payload.'
        }), 422


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': 'No carrier image file was uploaded.'}), 400

    file = request.files['file']
    passphrase = request.form.get('passphrase', '').strip()
    message = request.form.get('message', '')

    if not file or file.filename == '':
        return jsonify({'ok': False, 'error': 'Please select a carrier image.'}), 400

    if not passphrase:
        return jsonify({'ok': False, 'error': 'Please enter a secret passphrase.'}), 400

    if not message.strip():
        return jsonify({'ok': False, 'error': 'Please enter a message to encode.'}), 400

    original_filename = file.filename
    file_path = save_temp_upload(file)
    output = encode_image(image_path=file_path, message=message, passphrase=passphrase)

    if output and os.path.exists(output):
        # Remove the original upload immediately; remove the encoded output after sending
        remove_file_safely(file_path)

        @after_this_request
        def cleanup_files(response):
            remove_file_safely(output)
            return response

        download_name = build_download_name(original_filename)
        return send_file(
            output,
            as_attachment=True,
            download_name=download_name,
            mimetype='image/png'
        )
    else:
        remove_file_safely(file_path)
        remove_file_safely(output)
        return jsonify({'ok': False, 'error': 'Failed to encode the message into the image.'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', debug=debug, port=port)
