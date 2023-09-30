import React, { useRef } from 'react';
import Webcam from 'react-webcam';
import { BsCamera } from 'react-icons/bs';
import axios from 'axios'; // Import axios
import "./Webcam.css"

import faceOutline from './overlay.png'; // Import the outline image

const WebcamCapture = () => {
  const webcamRef = useRef(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    try {
      // Send the captured image to the backend
      console.log("WORK??")
      const response = await axios.post('http://127.0.0.1:5000/api/upload', { image: imageSrc });
      console.log('Image uploaded successfully:', response.data);

    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div className='webcam-container'>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <div className="overlay">
        <img src={faceOutline} alt="Outline" />
      </div>
      <button onClick={capture} id='capture-button'><BsCamera size={30}/></button>
    </div>
  );
};

export default WebcamCapture;
