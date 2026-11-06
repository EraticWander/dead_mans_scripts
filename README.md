# Dead Man's Scripts (`dead_mans_scripts`)

A Flask web application and utility suite for encrypting and hiding secret messages or files inside images using cryptographic steganography (`cryptosteganography`), paired with a TrueNAS API v2.0 integration client for automated NAS dataset/system management.

---

## Features

- **Cryptographic Image Steganography (`imageencryptor.py`)**:
  - Embeds AES-256 encrypted text messages or binary files inside carrier PNG images using LSB steganography.
  - Extracts and decrypts hidden payloads using a user-supplied passphrase.
- **Flask Web Interface (`app.py`)**:
  - Unified **Decode → Edit → Re-Encode** single-page studio interface with drag-and-drop image preview.
  - Upload an encoded PNG with its passphrase to decode the hidden message directly into the editor, make changes in-place, and re-encode/download the updated PNG with one click.
  - Or upload any carrier image, compose a new message, and download the steganographically encoded PNG.
  - Automatic post-request file cleanup (`@after_this_request` / `finally`) so sensitive original and encrypted images are removed from the server immediately after transmission.
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
├── Dockerfile             # Production container image definition
├── docker-compose.yml     # Docker Compose service configuration
├── .dockerignore          # Build context exclusions
├── init.sh                # Legacy container/system bootstrap script
├── requirements.txt       # Python dependencies
└── templates/             # Jinja2 HTML templates
    ├── base.html
    ├── upload.html        # Unified Decode, Edit & Re-Encode Stego Studio UI
    └── decrypt.html       # Legacy decode template
```

---

## Configuration

Create a `.env` file in the project root (optional, required only for the TrueNAS API client):

```env
HOST=192.168.1.100
API_KEY=your_truenas_api_key
```

---

## Installation & Usage

### Option 1: Docker Compose (Recommended)

```bash
# Build and start in the background (maps host port 5000 -> container port 80)
docker compose up -d --build

# Or specify a custom host port (e.g., port 8080):
HOST_PORT=8080 docker compose up -d --build

# Stop the container:
docker compose down
```

### Option 2: Docker CLI (`docker build` & `docker run`)

```bash
# 1. Build the Docker image
docker build -t dead_mans_scripts:latest .

# 2. Run the container on http://localhost:5000
docker run -d \
  --name dead_mans_scripts \
  --restart unless-stopped \
  -p 5000:80 \
  dead_mans_scripts:latest

# (Optional) Pass a .env file for TrueNAS API credentials:
docker run -d \
  --name dead_mans_scripts \
  --restart unless-stopped \
  --env-file .env \
  -p 5000:80 \
  dead_mans_scripts:latest
```

### Option 3: Local Python Setup

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
PORT=5000 python app.py
```

### Web Interface & API Endpoints

Once running, open `http://localhost:5000` in your browser:
- `GET /`: Unified Decode, Edit & Re-Encode Stego Studio workspace.
- `POST /api/decrypt`: Extract and decrypt a hidden message from an uploaded PNG (returns JSON).
- `POST /api/encrypt`: Encrypt and hide a message inside an uploaded carrier image (streams PNG download).

---

## Credits, Acknowledgments & External Sources

- **[`cryptosteganography`](https://github.com/computationalcore/cryptosteganography)** *(MIT License)*  
  Created by **computationalcore**. Provides the high-level Python interface for encrypting messages/files with AES-256 and embedding them inside images.
- **[`Stegano`](https://github.com/cedricbonhomme/Stegano)** *(GPL-3.0 License)* & **[`PyCryptodome`](https://github.com/Legrandin/pycryptodome)** *(BSD-2-Clause License)*  
  Authored by **Cédric Bonhomme** (`Stegano`) and **Helder Eijs** (`PyCryptodome`), providing the underlying Least Significant Bit (LSB) steganography algorithms and AES cryptographic primitives used by `cryptosteganography`.
- **[TrueNAS REST API v2.0](https://www.truenas.com/docs/api/)**  
  Official REST API specification by **iXsystems** used by `truenas_api.py` for automated NAS management.
- **[Flask](https://github.com/pallets/flask)** *(BSD-3-Clause License)* & **[`python-dotenv`](https://github.com/theskumar/python-dotenv)** *(BSD-3-Clause License)*  
  Web framework by the **Pallets Projects** and environment configuration loader by **Saurabh Kumar**.
