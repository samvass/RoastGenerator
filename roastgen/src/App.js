import './App.css';
import WebcamCapture from './webcam/Webcam';
import { useState } from 'react';


function App() {
  const [generatedText, setGeneratedText] = useState('');

    return (
      <div className='app-container'>
        <h1>Roast your friends, blame AI</h1>
        <WebcamCapture />
        {generatedText}
      </div>
    );
  }


export default App;
