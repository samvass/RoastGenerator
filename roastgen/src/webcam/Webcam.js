import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import html2canvas from 'html2canvas';
import download from 'downloadjs';
import { BsCamera } from 'react-icons/bs'; 
import "./Webcam.css"

import faceOutline from './overlay.png'; // Import the outline image

const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
  };

  const saveImage = () => {
    // if (capturedImage) {
    //   html2canvas(document.querySelector('#capture')).then((canvas) => {
    //     const ctx = canvas.getContext('2d');
    //     const image = new Image();
    //     image.src = capturedImage;

    //     // Draw the captured image on the canvas
    //     ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

    //     // Draw the outline on top of the captured image
    //     const outline = new Image();
    //     outline.src = faceOutline;
    //     ctx.drawImage(outline, 0, 0, canvas.width, canvas.height);

    //     // Save the canvas as an image
    //     download(canvas.toDataURL(), 'captured-image.png');
    //   });
    // }
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
      {/* {capturedImage && (
        <div id="capture">
          <img src={capturedImage} alt="Captured" />
          <button onClick={saveImage}>{BsCamera}</button>
        </div>
      )} */}
    </div>
  );
};

export default WebcamCapture;
