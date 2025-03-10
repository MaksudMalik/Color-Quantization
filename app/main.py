from fastapi import FastAPI, File, UploadFile, Form, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.process import process_image
import numpy as np
import base64
import cv2
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg"}

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(request: Request, file: UploadFile = File(...)):
    if file.content_type.lower() not in ALLOWED_MIME_TYPES:
        return JSONResponse(content={"error_message": "UPLOAD A VALID PHOTO"}, status_code=400)

    contents = await file.read()
    img_buffer = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
    _, image = cv2.imencode('.png', image)
    image = base64.b64encode(image).decode('utf-8')

    return JSONResponse(content={"original_img_base64": image})

@app.post("/quantize")
async def quantize_image(request: Request, num_colors: int = Form(...), iterations: int = Form(...), img_base64: str = Form(...)):
    original_data = base64.b64decode(img_base64)
    img_buffer = np.frombuffer(original_data, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    quantized_img = process_image(image, num_colors, iterations)

    _, proc_buffer = cv2.imencode('.png', quantized_img)
    processed_img_base64 = base64.b64encode(proc_buffer).decode('utf-8')

    return JSONResponse(content={
        "processed_img_base64": processed_img_base64
    })
