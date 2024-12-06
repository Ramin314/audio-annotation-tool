from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Segment(Base):
    __tablename__ = "segments"
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(String, index=True, nullable=False)
    start = Column(Float, nullable=False)
    end = Column(Float, nullable=False)
    transcript = Column(String, nullable=False)
    audio_file_id = Column(Integer, ForeignKey("audio_files.id"), nullable=True)

class AudioFile(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(String, unique=True, index=True, nullable=False)
    object_store_key = Column(String, unique=True, nullable=False)
    segments = relationship("Segment", backref="audio_file")
