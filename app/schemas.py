from pydantic import BaseModel

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
