from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
import shutil
from typing import List
import boto3
import uuid
from botocore.exceptions import NoCredentialsError

from backend import database as db

video_router = APIRouter(prefix="/videos", tags=["Videos"])

#to do use launch darkly here
s3_client = boto3.client(
    's3',
    aws_access_key_id= "ASIATFO246XVKAH7IUER",
    aws_secret_access_key= "WXqcc1pzWJPny001X7kTA7nqr3kySOwuY1ydWO0f",
    )

BUCKET_NAME = "fieldrocket-video-bucket-hackathon"

@video_router.post("/upload", status_code=201)
async def upload_video(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, unique_filename)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
        return {"filename": unique_filename, "url": file_url}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

