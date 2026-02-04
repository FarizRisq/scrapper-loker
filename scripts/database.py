import os
from google.cloud import storage
from dotenv import load_dotenv

# Ambil konfigurasi dari file .env
load_dotenv()

def upload_to_gcs(local_file_path, destination_blob_name):
    """Mengunggah file dari lokal Codespaces ke GCS Bucket."""
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    
    # Inisialisasi client GCS
    # Secara otomatis membaca path JSON dari GOOGLE_APPLICATION_CREDENTIALS di .env
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"Sedang mengunggah {local_file_path} ke GCS...")
    blob.upload_from_filename(local_file_path)
    print(f"Selesai! File tersedia di gs://{bucket_name}/{destination_blob_name}")
