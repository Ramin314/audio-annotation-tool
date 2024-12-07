import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import Waveform from './Waveform';

const AudioFileDetail = () => {
  const { id } = useParams();
  const [segments, setSegments] = useState([]);
  const [audioFileUrl, setAudioFileUrl] = useState(null);
  const [waveSurfer, setWaveSurfer] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const fetchSegments = async () => {
      try {
        const response = await fetch(`http://localhost:5000/audio-files/${id}/segments/`);
        if (!cancelled) {
          const data = await response.json();
          setSegments(data);
        }
      } catch (error) {
        if (!cancelled) console.error('Error fetching segments:', error);
      }
    };

    const fetchAudioFile = async () => {
      try {
        const response = await fetch(`http://localhost:5000/audio-files/${id}`);
        if (!cancelled) {
          const data = await response.json();
          const url = `http://localhost:9000/audio-files/${data.object_store_key}`;
          setAudioFileUrl(url);
        }
      } catch (error) {
        if (!cancelled) console.error('Error fetching audio file:', error);
      }
    };

    fetchSegments();
    fetchAudioFile();

    return () => {
      cancelled = true;
    };
  }, [id]);

  const handleWaveformReady = useCallback((ws) => {
    console.log('WaveSurfer is ready in parent, duration:', ws.getDuration());
    setWaveSurfer(ws);
  }, []);

  const seekToTime = (time) => {
    if (waveSurfer) {
      const duration = waveSurfer.getDuration();
      if (duration > 0) {
        const progress = Math.min(Math.max(time / duration, 0), 1);
        console.log(`Seeking to ${time}s (progress: ${progress})`);
        waveSurfer.seekTo(progress);
      } else {
        console.warn('Duration is 0, cannot seek yet');
      }
    } else {
      console.warn('WaveSurfer not ready yet');
    }
  };

  return (
    <div>
      <h1>Segments for Audio File ID: {id}</h1>

      {audioFileUrl ? (
        <Waveform audio={audioFileUrl} onReady={handleWaveformReady} />
      ) : (
        <p>Loading waveform...</p>
      )}

      <ul>
        {segments.map((segment) => (
          <li key={segment.id}>
            <strong>Start:</strong>{' '}
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                seekToTime(segment.start);
              }}
            >
              {segment.start}s
            </a>
            , <strong>End:</strong>{' '}
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                seekToTime(segment.end);
              }}
            >
              {segment.end}s
            </a>
            , <strong>Transcript:</strong> {segment.transcript}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AudioFileDetail;
