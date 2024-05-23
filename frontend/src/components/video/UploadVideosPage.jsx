import React, { useState } from 'react';

const VideoUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prompt, setPrompt] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('prompt', prompt);
    debugger;
    try {
      const response = await fetch('http://localhost:8000/videos/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        alert('Video uploaded successfully!');
      } else {
        alert('Failed to upload video');
      }
    } catch (error) {
      console.error('Error uploading video:', error);
      alert('Error uploading video');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <div className="mb-6">
        <label
          htmlFor="videoUpload"
          className="flex items-center justify-center w-full px-4 py-2 tracking-wide text-white uppercase bg-blue-500 border border-blue-500 rounded-lg cursor-pointer hover:bg-blue-600 hover:border-blue-600"
        >
          <svg
            className="w-6 h-6 mr-2"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
          >
            <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
          </svg>
          <span className="text-base leading-normal">Select a video</span>
          <input type="file" id="videoUpload" accept="video/*" onChange={handleFileChange} className="hidden" />
        </label>
      </div>
      <div className="mb-6">
        <label htmlFor="promptInput" className="block mb-2 font-bold text-gray-700">
          Prompt:
        </label>
        <input
          type="text"
          id="promptInput"
          value={prompt}
          onChange={handlePromptChange}
          placeholder="What finished video would you like to make?"
          className="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none"
        />
      </div>
      <button
        type="submit"
        className="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:outline-none"
      >
        Upload
      </button>
    </form>
  );
};

export default VideoUpload;