import os
import requests
import sys
import time
from tqdm import tqdm

EMBEDDING_URL = os.environ.get('EMBEDDING_URL')

CHUNK_SIZE = 1024 * 1024

def get_filename(MODEL_URL):
    if '.safetensors' in MODEL_URL:
        return 'embeddings/embed.safetensors'
    else:
        return 'embeddings/embed.ckpt'

def check_model_file(filename):
    file_size_mb = round(os.path.getsize(filename) / (1024 * 1024))
    if file_size_mb < 100:
        print(f'The downloaded file is only {file_size_mb} MB and does not appear to be a valid model.')
        sys.exit(1)

def download_embed_file(EMBED_URL):
    filename = get_filename(EMBED_URL)
    print('filename:', filename)
    response = requests.get(EMBED_URL, stream=True)
    with open(filename, 'wb') as f, tqdm(desc="Downloading", unit="bytes", total=int(response.headers.get('content-length', 0))) as progress:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))


download_embed_file(EMBEDDING_URL)