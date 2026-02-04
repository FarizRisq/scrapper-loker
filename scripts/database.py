import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def upload_to_gcs(local_file_path, destination_blob_name):
    # 1. Ambil rahasia dari environment variable (GitHub Secrets)
    gcp_json_string = os.getenv("GCP_KEY_JSON")
    bucket_name = os.getenv("GCS_BUCKET_NAME")

    if not gcp_json_string:
        print("Error: GCP_KEY_JSON tidak ditemukan di Secrets!")
        return

    # 2. Ubah string JSON jadi kredensial resmi Google
    info = json.loads(gcp_json_string)
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 3. Koneksi ke GCS
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # 4. Upload!
    print(f"Mengunggah {local_file_path} ke GCS...")
    blob.upload_from_filename(local_file_path)
    print(f"Sukses! Cek di bucket: {bucket_name}")
