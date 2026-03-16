import React, { useState, useEffect } from "react";

const Typewriter = ({ text, delay, onComplete }) => {
  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setCurrentText((prevText) => prevText + text[currentIndex]);
        setCurrentIndex((prevIndex) => prevIndex + 1);
      }, delay);
      return () => clearTimeout(timeout);
    } else if (currentIndex === text.length && text.length > 0) {
      const timeout = setTimeout(() => {
        setVisible(false);
        if (onComplete) onComplete();
      }, 1000);
      return () => clearTimeout(timeout);
    }
  }, [currentIndex, delay, text]);

  if (!visible) return null;

  return <span style={{opacity: visible ? 1 : 0, transition : 'opacity 0.8s ease'}}>{currentText}</span>;
};

export default Typewriter;
