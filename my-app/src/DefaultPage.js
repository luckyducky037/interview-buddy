import React, { useState } from 'react'
import './DefaultPage.css';

function DefaultPage() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleButtonClick = () => {
    document.getElementById('fileInput').click();
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setResponse(null);

  const formData = new FormData();
  if (!file) {
    setError("Please select a file before uploading.");
    return;
  }
  formData.append("file", file);

  try {
    const res = await fetch("http://localhost:4000/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorText = await res.text(); // Capture error message from the backend
      throw new Error(`Server error: ${errorText}`);
    }

    const data = await res.json();
    setResponse(data);
  } catch (error) {
    console.error("Error during upload:", error);
    setError("Failed to upload file. Please try again or check the server.");
  }
};

  return (
    <div>
      <title>Interview Helper</title>
        <h1 className="text">Interview Helper</h1>
        <h2 className="text">Submit audio files below</h2>
        
      
        <form className="text" onSubmit={handleSubmit}>
          <label htmlFor="fileInput">Choose an audio file: </label>
          <br/>
          <input
            type="file"
            id="fileInput"
            name="file"
            accept="audio/*"
            className="file-input"
            onChange={handleFileChange}
          />
          <br />
          <button type="button" className="custom-button" onClick={handleButtonClick}>
            {file ? file.name : "Browse"}
          </button>
          <br /><br />
          <input id="submit-button" type="submit" value="Upload" />
        </form>

        <div className="feedback-container">
          <label className="feedback-label" htmlFor="feedback">Feedback</label>
          <textarea id="feedback" className="feedback-box" value={response ? JSON.stringify(response, null, 2) : ''} readOnly></textarea>
        </div>
    </div>
  );
}

export default DefaultPage