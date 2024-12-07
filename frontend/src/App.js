import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AudioFileList from './components/AudioFileList';
import AudioFileDetail from './components/AudioFileDetail';
import 'semantic-ui-css/semantic.min.css';
import './App.css';

function App() {
  return (
    <div className="ui container" style={{ padding: '2rem' }}>
    <div>
    <div className="ui container center aligned" style={{ padding: '1rem 0' }}>
      <a style={{ color: 'rgba(0,0,0,.87)' }} href='/'>
      <h1 className="header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <img
          src="/logo.png"
          alt="Logo"
          style={{ height: '50px', marginRight: '10px' }}
        />
        Annotation Tool
      </h1>
      </a>
    </div>
    </div>
    <Router>
      <Routes>
        <Route path="/" element={<AudioFileList />} />
        <Route path="/:id" element={<AudioFileDetail />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;
