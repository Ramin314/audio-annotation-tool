import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import Pagination from './Pagination';

const AudioFileList = () => {
  const [audioFiles, setAudioFiles] = useState([]);
  const [hasMore, setHasMore] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const currentPage = parseInt(searchParams.get('page') || '1', 10); // Default to page 1

  const fetchAudioFiles = async (page) => {
    const response = await fetch(`http://localhost:5000/audio-files/?skip=${(page - 1) * 10}&limit=10`);
    const data = await response.json();
    setAudioFiles(data);
    setHasMore(data.length === 10); // If 4 items are returned, assume there may be more
  };

  useEffect(() => {
    fetchAudioFiles(currentPage);
  }, [currentPage]);

  const setCurrentPage = (page) => {
    setSearchParams({ page });
  };

  return (
      <>
      <h2 className="ui header">Audio Files</h2>
      <div className="ui relaxed divided list">
        {audioFiles.map((file) => (
          <div className="item" key={file.recording_id}>
            <div className="content">
              <br />
              <a href={`/${file.recording_id}`} className="header purple">
                Audio File ID: {file.recording_id}
              </a>
              <div className="description" style={{ fontSize: '0.9em', color: 'gray' }}>
                Labeled Segments: {file.labeled_segments}/{file.total_segments}
              </div>
              <br />
            </div>
          </div>
        ))}
      </div>
      <Pagination currentPage={currentPage} hasMore={hasMore} setCurrentPage={setCurrentPage} />
      </>
  );
};

export default AudioFileList;
