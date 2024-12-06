from sqlalchemy.orm import Session
from . import models, schemas, enums
from typing import Optional

# Segments

def get_segment(db: Session, id: int):
    return db.query(models.Segment).get(id)

def get_segments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Segment).offset(skip).limit(limit).all()

def get_segments_by_recording_id(db: Session, recording_id: str):
    return db.query(models.Segment).filter(models.Segment.recording_id == recording_id).all()

def create_segment(db: Session, segment: schemas.SegmentCreate):
    db_segment = models.Segment(**segment.dict())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

# Audio Files

def get_audio_files(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.AudioFile).offset(skip).limit(limit).all()

def get_audio_file_by_recording_id(db: Session, recording_id: str):
    return db.query(models.AudioFile).filter(models.AudioFile.recording_id == recording_id).first()

def create_audio_file(db: Session, recording_id: str, object_store_key: str):
    db_audio_file = models.AudioFile(
        recording_id=recording_id,
        object_store_key=object_store_key
    )
    db.add(db_audio_file)
    db.commit()
    db.refresh(db_audio_file)
    return db_audio_file

# Annotations

def update_segment_annotation(db: Session, segment_id: int, annotation: Optional[enums.AnnotationEnum]):
    segment = db.query(models.Segment).filter(models.Segment.id == segment_id).first()
    if not segment:
        return None
    segment.annotation = annotation
    db.commit()
    db.refresh(segment)
    return segment
