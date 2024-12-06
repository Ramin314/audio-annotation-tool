import os
import csv
from minio import Minio
from sqlalchemy.orm import Session
from . import schemas, crud

MINIO_URL = "minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "audio-files"

minio_client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

def ensure_bucket_exists():
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

def upload_audio_to_minio(file_path: str, file_name: str):
    ensure_bucket_exists()
    minio_client.fput_object(BUCKET_NAME, file_name, file_path)

def process_segments_directory(csv_directory: str, audio_directory: str, db: Session):
    for file_name in os.listdir(csv_directory):
        if file_name.endswith(".csv"):
            csv_path = os.path.join(csv_directory, file_name)
            process_csv(csv_path, audio_directory, db)

def process_csv(csv_path: str, audio_directory: str, db: Session):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recording_id = row['recording_id']
            start = float(row['start'])
            end = float(row['end'])
            transcript = row['transcript']

            existing_segments = crud.get_segments_by_recording_id(db, recording_id)
            if any(segment.start == start and segment.end == end for segment in existing_segments):
                continue

            audio_file = crud.get_audio_file_by_recording_id(db, recording_id)
            if not audio_file:
                audio_file_path = os.path.join(audio_directory, f"{recording_id}.wav")
                if os.path.exists(audio_file_path):
                    object_store_key = f"{recording_id}.wav"
                    upload_audio_to_minio(audio_file_path, object_store_key)
                    audio_file = crud.create_audio_file(db, recording_id, object_store_key)
                else:
                    print(f"Audio file {recording_id}.wav not found. Skipping.")

            segment = schemas.SegmentCreate(
                recording_id=recording_id,
                start=start,
                end=end,
                transcript=transcript
            )
            crud.create_segment(db, segment)
