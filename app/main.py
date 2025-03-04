from fastapi import FastAPI, File, UploadFile, Form, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.process import process_image
import numpy as np
import base64
import cv2
import os

app = FastAPI()
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

image_storage = {"original": None}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg"}

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "original_img_base64": image_storage["original"]})

@app.post("/upload")
async def upload_image(request: Request, file: UploadFile = File(...)):
    if file.content_type.lower() not in ALLOWED_MIME_TYPES:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error_message": "UPLOAD A VALID PHOTO"},
        )
    contents = await file.read()
    img_buffer = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    _, buffer = cv2.imencode('.png', image)
    image_storage["original"] = base64.b64encode(buffer).decode('utf-8')

    return RedirectResponse(url="/", status_code=303)

@app.post("/quantize")
async def quantize_image(request: Request, num_colors: int = Form(...), iterations: int = Form(...)):
    if not image_storage["original"]:
        return RedirectResponse(url="/", status_code=303)

    original_data = base64.b64decode(image_storage["original"])
    img_buffer = np.frombuffer(original_data, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    quantized_img = process_image(image, num_colors, iterations)

    _, proc_buffer = cv2.imencode('.png', quantized_img)
    processed_img_base64 = base64.b64encode(proc_buffer).decode('utf-8')

    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "original_img_base64": image_storage["original"],
            "processed_img_base64": processed_img_base64,
        }
    )
