import React, { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom'; // ✅ No BrowserRouter here

import './App.css';
import './components/HeaderFile/HeaderStyle.css';

import HeaderFile from './components/HeaderFile/HeaderFile';
import SocialMedia from './components/SocialMedia/SocialMedia';
import InputText from './components/InputText/InputText';
import ImagePage from './components/ImagePage/ImagePage';

function App() {
  const [mode, setMode] = useState('Dark');

  useEffect(() => {
    document.body.style.backgroundColor = mode === 'Dark' ? '#343541' : 'white';
  }, [mode]);

  const changeMode = () => {
    setMode((prevMode) => (prevMode === 'Light' ? 'Dark' : 'Light'));
  };

  return (
    <div className={`App-${mode}`}>
      <div className={`social-media-${mode}`}>
        <div className="right-items">
          <SocialMedia Theme={mode} />
        </div>
        <div className="center-items">
          <HeaderFile mode={mode} />
        </div>
        <div className="left-items">
          <button className={`mode-${mode}`} onClick={changeMode}></button>
        </div>
      </div>

      <div className="main-content">
        <Routes>
          <Route path="/" element={<InputText mode={mode} />} />
          <Route path="/upload" element={<ImagePage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
