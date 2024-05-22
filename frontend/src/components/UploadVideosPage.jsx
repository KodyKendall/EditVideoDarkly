import React, { useState } from 'react';

const VideoUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!selectedFile) {
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append('video', selectedFile);

        try {
            const response = await fetch('http://PENDING', {
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
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="videoUpload">Upload Video:</label>
                <input
                    type="file"
                    id="videoUpload"
                    accept="video/*"
                    onChange={handleFileChange}
                />
            </div>
            <button type="submit">Upload</button>
        </form>
    );
};

export default VideoUpload;
