import './App.css';
import WebcamCapture from './webcam/Webcam';
import { BsCamera } from 'react-icons/bs'; 

function App() {

    return (
      <div className='app-container'>
        <h1>Roast your friends, blame AI</h1>
        <WebcamCapture />
      </div>
    );
  }


export default App;
