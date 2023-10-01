import "./App.css";
import WebcamCapture from "./webcam/Webcam";
import { useState } from "react";

function App() {
  const [generatedText, setGeneratedText] = useState("");

  return (
    <div className='app-container'>
      <h1>roast your friends, blame AI</h1>
      <WebcamCapture setGeneratedText={setGeneratedText} />

      {generatedText && (
        <div
          style={{
            margin: "80px",
            fontSize: "30px",
            fontWeight: "500",
            backgroundColor: "white",
            borderRadius: "20px",
            padding: "80px",
          }}
        >
          {generatedText}
        </div>
      )}
    </div>
  );
}

export default App;
