import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { BsCamera } from 'react-icons/bs';
import { GrPowerReset } from 'react-icons/gr';

import axios from 'axios'; // Import axios
import "./Webcam.css"
import html2canvas from 'html2canvas'; // Import html2canvas

import faceOutline from './overlay.png'; // Import the outline image

const WebcamCapture = (props) => {
  const webcamRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null)

  const saveImage = () => {
    if (capturedImage) {
      html2canvas(document.querySelector('#capture')).then((canvas) => {
        const ctx = canvas.getContext('2d');
        const image = new Image();
        image.src = capturedImage;

        // Draw the captured image on the canvas
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

        // Draw the outline on top of the captured image
        const outline = new Image();
        outline.src = faceOutline;
        ctx.drawImage(outline, 0, 0, canvas.width, canvas.height);
      });
    }
  };

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);

    try {
      // Send the captured image to the backend
      const response = await axios.post('http://127.0.0.1:5000/api/upload', { image: imageSrc });
      props.setGeneratedText(response.data.output_text)
      console.log('Image uploaded successfully:', response.data);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div className='webcam-container'>
      {!capturedImage && <Webcam
        audio={false}
        ref={webcamRef}
        mirrored={true}
        screenshotFormat="image/jpeg"
      />}
      {!capturedImage && <div className="overlay">
        <img src={faceOutline} alt="Outline" />
      </div>}
      {!capturedImage && <button onClick={capture} id='capture-button'><BsCamera size={30}/></button>}
      
      
      {capturedImage && (
        <div id="capture">
          <img src={capturedImage} alt="Captured" />
        </div>
      )}
      {capturedImage && <button onClick={() => setCapturedImage(false)} id='reset-button'><GrPowerReset size={30}/></button>}
      
    </div>
  );
};

export default WebcamCapture;
