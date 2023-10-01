import './App.css';
import WebcamCapture from './webcam/Webcam';
import { useState } from 'react';


function App() {
  const [generatedText, setGeneratedText] = useState('');

  const setText = (text) => {
    console.log(text)
  }

    return (
      <div className='app-container'>
        <h1>Roast your friends, blame AI</h1>
        <WebcamCapture setText={setText} setGeneratedText={setGeneratedText}  />
          {generatedText}
      </div>
    );
  }


export default App;
