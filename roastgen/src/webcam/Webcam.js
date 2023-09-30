import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import html2canvas from 'html2canvas';
import download from 'downloadjs';
import { BsCamera } from 'react-icons/bs'; 
import "./Webcam.css"

const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
  };

  const saveImage = () => {
    if (capturedImage) {
      html2canvas(document.querySelector('#capture')).then((canvas) => {
        download(canvas.toDataURL(), 'captured-image.png');
      });
    }
  };

  return (
    <div className='webcam-container'>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
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
