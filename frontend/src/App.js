import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AudioFileList from './components/AudioFileList';
import AudioFileDetail from './components/AudioFileDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AudioFileList />} />
        <Route path="/:id" element={<AudioFileDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
