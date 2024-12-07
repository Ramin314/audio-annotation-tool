from sqlalchemy.orm import Session
from . import models, schemas, enums
from typing import Optional
from sqlalchemy.sql import func, case, asc, cast
from sqlalchemy.types import Numeric

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
    labeled_case = case((models.Segment.annotation.isnot(None), 1), else_=0)
    total_count = func.count(models.Segment.id)
    labeled_sum = func.sum(labeled_case)

    ratio = case(
        (total_count == 0, 1.0),
        else_=cast(labeled_sum, Numeric) / cast(total_count, Numeric)
    )

    results = (
        db.query(
            models.AudioFile.recording_id,
            models.AudioFile.id,
            models.AudioFile.object_store_key,
            total_count.label("total_segments"),
            labeled_sum.label("labeled_segments"),
            ratio.label("labeled_ratio")
        )
        .outerjoin(models.Segment, models.AudioFile.recording_id == models.Segment.recording_id)
        .group_by(models.AudioFile.id)
        .order_by(asc(ratio))
        .offset(skip)
        .limit(limit)
        .all()
    )

    labeled_stats = []
    for result in results:
        percent = float(result.labeled_ratio) * 100
        labeled_stats.append({
            "id": result.id,
            "object_store_key": result.object_store_key,
            "recording_id": result.recording_id,
            "total_segments": result.total_segments,
            "labeled_segments": result.labeled_segments,
            "unlabeled_segments": result.total_segments - result.labeled_segments,
            "labeled_percentage": percent,
        })

    return labeled_stats

def get_audio_file_by_recording_id(db: Session, recording_id: str):
    labeled_case = case((models.Segment.annotation.isnot(None), 1), else_=0)
    total_count = func.count(models.Segment.id)
    labeled_sum = func.sum(labeled_case)

    ratio = case(
        (total_count == 0, 1.0),
        else_=cast(labeled_sum, Numeric) / cast(total_count, Numeric)
    )

    result = (
        db.query(
            models.AudioFile.id.label("audio_file_id"),
            models.AudioFile.recording_id,
            models.AudioFile.object_store_key,
            total_count.label("total_segments"),
            labeled_sum.label("labeled_segments"),
            ratio.label("labeled_ratio")
        )
        .outerjoin(models.Segment, models.AudioFile.recording_id == models.Segment.recording_id)
        .filter(models.AudioFile.recording_id == recording_id)
        .group_by(models.AudioFile.id)
        .first()
    )

    if not result:
        return None

    labeled_percentage = float(result.labeled_ratio) * 100

    return {
        "id": result.audio_file_id,
        "object_store_key": result.object_store_key,
        "recording_id": result.recording_id,
        "total_segments": result.total_segments,
        "labeled_segments": result.labeled_segments,
        "unlabeled_segments": result.total_segments - result.labeled_segments,
        "labeled_percentage": labeled_percentage,
    }

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
