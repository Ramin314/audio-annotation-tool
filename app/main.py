from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database
from .utils import process_segments_directory

from . import crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

DATA_DIR = "data/segments"
AUDIO_DIR = "data/audio"

def session():
    yield database.SessionLocal()

@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    process_segments_directory(DATA_DIR, AUDIO_DIR, db)
    db.close()

# Segments

@app.post("/segments/", response_model=schemas.Segment)
def create_segment(segment: schemas.SegmentCreate, db = Depends(session)):
    return crud.create_segment(db=db, segment=segment)

@app.get("/segments/", response_model=list[schemas.Segment])
def read_segments(skip: int = 0, limit: int = 10, db: Session = Depends(session)):
    return crud.get_segments(db=db, skip=skip, limit=limit)

# Audio

@app.post("/audio-files/", response_model=schemas.AudioFile)
def create_audio_file(recording_id: str, object_store_key: str, db = Depends(session)):
    return crud.create_audio_file(db=db, recording_id=recording_id, object_store_key=object_store_key)

@app.get("/audio-files/", response_model=list[schemas.AudioFile])
def read_audio_files(skip: int = 0, limit: int = 10, db = Depends(session)):
    return crud.get_audio_files(db=db, skip=skip, limit=limit)

@app.get("/audio-files/{id}/", response_model=schemas.AudioFile)
def read_audio_file(id: str, db: Session = Depends(session)):
    audio_file = crud.get_audio_file_by_recording_id(db=db, recording_id=id)
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return audio_file

@app.get("/audio-files/{id}/segments/", response_model=list[schemas.Segment])
def read_segments_by_audio_file_id(id: str, db: Session = Depends(session)):
    audio_file = crud.get_audio_file_by_recording_id(db=db, recording_id=id)
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    segments = crud.get_segments_by_recording_id(db=db, recording_id=id)
    return segments
