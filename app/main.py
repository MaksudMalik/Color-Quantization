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
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg"}

@app.get("/")
async def homepage(request: Request):
    original_img = request.cookies.get("original_img")
    processed_img = request.cookies.get("processed_img")
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "original_img_base64": original_img,
        "processed_img_base64": processed_img,
    })

@app.post("/upload")
async def upload_image(request: Request, file: UploadFile = File(...)):
    if file.content_type.lower() not in ALLOWED_MIME_TYPES:
        return templates.TemplateResponse("index.html", {"request": request, "error_message": "UPLOAD A VALID PHOTO"})

    contents = await file.read()
    img_buffer = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    _, buffer = cv2.imencode('.png', image)
    encoded_img = base64.b64encode(buffer).decode('utf-8')

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="original_img", value=encoded_img, httponly=True, max_age=3600)
    return response

@app.post("/quantize")
async def quantize_image(request: Request, num_colors: int = Form(...), iterations: int = Form(...)):
    original_img = request.cookies.get("original_img")
    if not original_img:
        return RedirectResponse(url="/", status_code=303)

    original_data = base64.b64decode(original_img)
    img_buffer = np.frombuffer(original_data, np.uint8)
    image = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    quantized_img = process_image(image, num_colors, iterations)

    _, proc_buffer = cv2.imencode('.png', quantized_img)
    processed_img_base64 = base64.b64encode(proc_buffer).decode('utf-8')

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="processed_img", value=processed_img_base64, httponly=True, max_age=3600)
    return response
