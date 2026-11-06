# Dead Man's Scripts (`dead_mans_scripts`)

A Flask web application and utility suite for encrypting and hiding secret messages or files inside images using cryptographic steganography (`cryptosteganography`), paired with a TrueNAS API v2.0 integration client for automated NAS dataset/system management.

---

## Features

- **Cryptographic Image Steganography (`imageencryptor.py`)**:
  - Embeds AES-256 encrypted text messages or binary files inside carrier PNG images using LSB steganography.
  - Extracts and decrypts hidden payloads using a user-supplied passphrase.
- **Flask Web Interface (`app.py`)**:
  - Upload an image, enter a message and passphrase, and immediately download the steganographically encoded PNG.
  - Upload an encoded PNG with its passphrase to decode and view the secret message in the browser.
  - Automatic post-request file cleanup (`@after_this_request`) so sensitive original and encrypted images are removed from the server immediately after transmission.
- **TrueNAS REST API v2.0 Client (`truenas_api.py`)**:
  - Bearer token authentication against TrueNAS SCALE / CORE API v2.0 (`https://<HOST>/api/v2.0`).
  - Helpers for querying system info, pools, datasets, shares (SMB/NFS), snapshots, and user management.

---

## Project Structure

```text
dead_mans_scripts/
├── app.py                 # Flask web server for encoding/decoding steganographic images
├── imageencryptor.py      # CryptoSteganography wrapper class (encrypt/decrypt text & files)
├── truenas_api.py         # TrueNAS API v2.0 client wrapper
├── init.sh                # Container/system bootstrap script
├── requirements.txt       # Python dependencies
└── templates/             # Jinja2 HTML templates
    ├── base.html
    ├── upload.html        # Encode message into image UI
    └── decrypt.html       # Decode message from image UI
```

---

## Configuration

Create a `.env` file in the project root for the TrueNAS API client:

```env
HOST=192.168.1.100
API_KEY=your_truenas_api_key
```

---

## Installation & Usage

### Local Setup

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

The web interface will be available at `http://localhost:5000`:
- `GET /` & `POST /`: Encrypt and hide a message inside an uploaded image.
- `GET /decrypt` & `POST /decrypt`: Extract and decrypt a hidden message from an uploaded PNG.
