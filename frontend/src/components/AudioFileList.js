import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Pagination from './Pagination';

const AudioFileList = () => {
  const [audioFiles, setAudioFiles] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchAudioFiles = async (page) => {
    const response = await fetch(`http://localhost:5000/audio-files/?skip=${(page - 1) * 10}&limit=10`);
    const data = await response.json();
    setAudioFiles(data);
    setTotalPages(Math.ceil(data.total / 10)); // Assuming the API returns `total` for pagination
  };

  useEffect(() => {
    fetchAudioFiles(currentPage);
  }, [currentPage]);

  return (
    <div>
      <h1>Audio Files</h1>
      <ul>
        {audioFiles.map((file) => (
          <li key={file.recording_id}>
            <Link to={`/${file.recording_id}`}>Audio File ID: {file.recording_id}</Link> - 
            Labeled Segments: {file.labeled_segments}/{file.total_segments}
          </li>
        ))}
      </ul>
      <Pagination currentPage={currentPage} totalPages={totalPages} setCurrentPage={setCurrentPage} />
    </div>
  );
};

export default AudioFileList;
