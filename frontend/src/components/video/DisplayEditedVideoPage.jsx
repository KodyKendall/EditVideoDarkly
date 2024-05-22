import React from 'react';

const VideoDisplay = () => {
    const videoUrl = "https://fieldrocket-video-bucket-hackathon.s3.us-west-2.amazonaws.com/e3fe3bf9-c6c7-4bcc-9d03-baa11cde773a.mp4" ;

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <div className="w-full max-w-2xl bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-semibold mb-4">Video Display</h2>
                <div className="w-full">
                    <video controls width="100%" src={videoUrl} className="rounded-lg shadow-md" />
                </div>
            </div>
        </div>
    );
};

export default VideoDisplay;
