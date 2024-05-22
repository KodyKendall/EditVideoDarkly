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
    aws_session_token= "IQoJb3JpZ2luX2VjEOz//////////wEaCXVzLWVhc3QtMSJIMEYCIQDI4I+RPTavif6B4UBKkfU7+JP5gNOuBdIB9FbK+V6hYgIhAPsOfbOYdrPGsayquPgCFGZ/6ND/8i3R/SPfogvtXOJxKpkCCGUQARoMMjE3ODkxNzk2NDU4IgycQhMqtnUgVWoTenUq9gFexwOQbiebrZzR5/HclXWrYYhZ1l/AuYCyo6vU7F+mB++Sauxfl0CeoF00DMkTd7THV2hdFEsh76dkJyqolYhqXogze6+HZapZs419yQrLQ8q4HLzbnFed4ZGC6fKEMOwb2YFGM4ME2uVLo5HcxRObZUL4vJG8nRMa+4G1xWX2QAnvExUZOD2WrbQdRFXeEadNQ+1HuYSTavU+lgeoYNWNFpMJ4DDwAqSAmvsfBKwrfqL9yCY9j40F2TXipmmSEJdjlZ9SLtJlutJdCUgSOKuxno+CGyNyDuHoHZ54ytfeWcTu5V5XBA2emUo62ITW0je9ZnU3sKAwupq5sgY6nAHv/AMDkmdYMUvKGlMRmvhcqg7s6+5AYCEzbNyCPeJv0fMY1RbVQ14btNwAfQWPDHZjc9IvqngUa8L4D3iZDozz9yn3XuVGVWELNEkZYW736E9IVRQ2NKK83CCQj9OKvR6DKSjJJuoBgNqBjvv83ezKXdd7Wa7vTVe/fY2qGTO8XCNLgWNPAJ/jFO5JPqFkQ4Fzx92OuyYEtK1Q1v4=",
    )

BUCKET_NAME = "fieldrocket-video-bucket-hackathon"

@video_router.post("/upload", status_code=201)
async def upload_video(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, unique_filename)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
        print(file_url)
        return {"filename": unique_filename, "url": file_url}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

