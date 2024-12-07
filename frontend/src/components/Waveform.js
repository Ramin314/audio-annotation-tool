import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import WaveSurfer from 'wavesurfer.js';
import styled from 'styled-components';
import { FaPlayCircle, FaPauseCircle } from 'react-icons/fa';

const Waveform = ({ audio, onReady }) => {
  const containerRef = useRef(null);
  const waveSurferRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!audio) return;

    console.log('Initializing WaveSurfer for audio:', audio);

    const audioWithCacheBuster = `${audio}?cb=${Date.now()}`;

    const waveSurfer = WaveSurfer.create({
      container: containerRef.current,
      backend: 'WebAudio',
      responsive: true,
      barWidth: 2,
      cursorWidth: 1,
      height: 100,
    });

    waveSurfer.load(audioWithCacheBuster);

    waveSurfer.on('ready', () => {
      console.log('WaveSurfer ready. Duration:', waveSurfer.getDuration());
      waveSurferRef.current = waveSurfer;
      onReady && onReady(waveSurfer);
    });

    waveSurfer.on('error', (err) => {
      console.error('WaveSurfer error:', err);
    });

    waveSurfer.on('play', () => setIsPlaying(true));
    waveSurfer.on('pause', () => setIsPlaying(false));
    waveSurfer.on('finish', () => setIsPlaying(false));

    return () => {
      console.log('Destroying WaveSurfer instance');
      waveSurfer.destroy();
      waveSurferRef.current = null;
    };
  }, [audio, onReady]);

  const handlePlayPause = () => {
    if (waveSurferRef.current) {
      waveSurferRef.current.playPause();
    }
  };

  return (
    <WaveSurferWrap>
      <button onClick={handlePlayPause} type="button">
        {isPlaying ? <FaPauseCircle size="3em" color="#6e5bcb" /> : <FaPlayCircle size="3em" color="#6e5bcb" />}
      </button>
      <div ref={containerRef} style={{marginLeft: '30px'}} />
    </WaveSurferWrap>
  );
};

Waveform.propTypes = {
  audio: PropTypes.string.isRequired,
  onReady: PropTypes.func,
};

const WaveSurferWrap = styled.div`
  display: grid;
  grid-template-columns: 40px 1fr;
  align-items: center;

  button {
    width: 40px;
    height: 40px;
    border: none;
    padding: 0;
    background-color: white;
    cursor: pointer;
  }
`;

export default Waveform;
