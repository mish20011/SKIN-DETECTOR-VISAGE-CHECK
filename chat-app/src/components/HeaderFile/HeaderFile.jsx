import React, { useEffect } from 'react';
import './HeaderFile.css';


const Buzzwords = ({ mode }) => {
  useEffect(() => {
    const chars = document.querySelectorAll('.js_charTrigger');
    chars.forEach((char) => {
      char.addEventListener('mouseover', () => {
        char.classList.add('jumpingLetter');
      });
      char.addEventListener('animationend', () => {
        char.classList.remove('jumpingLetter');
      });
    });
  }, []);

  const text = "VISAGECHECK";

  return (
    <div className="c-buzzwords">
      {text.split(' ').map((word, wordIndex) => (
        <div key={wordIndex} className="c-buzzwords__word">
          {word.split('').map((char, charIndex) => (
            
            <span key={charIndex} className={`js_charTrigger c-buzzwords__charWrapper`}>
            <span className={`c-buzzwords__char header-${mode}`}>{char}</span>
          </span>
          
          ))}
        </div>
      ))}
    </div>
  );
};

export default Buzzwords;
