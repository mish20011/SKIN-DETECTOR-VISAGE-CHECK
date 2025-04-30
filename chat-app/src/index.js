import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import NoteState from './components/NoteState';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <NoteState>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </NoteState>
  </React.StrictMode>
);
