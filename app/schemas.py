from pydantic import BaseModel
from . import enums
from typing import Optional

# Annotations

class UpdateAnnotation(BaseModel):
    annotation: Optional[enums.AnnotationEnum] = None

# Segments

class SegmentBase(BaseModel):
    recording_id: str
    start: float
    end: float
    transcript: str

class SegmentCreate(SegmentBase):
    pass

class Segment(SegmentBase):
    id: int
    annotation: Optional[enums.AnnotationEnum] = None

    class Config:
        orm_mode = True

# Audio

class AudioFileBase(BaseModel):
    recording_id: str
    object_store_key: str

class AudioFileCreate(AudioFileBase):
    pass

class AudioFile(AudioFileBase):
    id: int

    class Config:
        orm_mode = True
