from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import hashlib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Form_={}

def generate_short_code(long_url):
    
    hash_object = hashlib.sha256(long_url.encode())
    short_code = hash_object.hexdigest()[0:6]
    return short_code

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request, url: str = Form(...)):
    try:
        short_code = generate_short_code(url)
        short_url = "https://shorten-url-henna.vercel.app/" + short_code
        Form_[short_code] = url  # 更新字典，使用 short_code 作為鍵
        return templates.TemplateResponse("result.html", {'request': request, "name": short_url})
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/{short_code}")
async def redirect_to_long_url(short_code:str):
    if short_code in Form_:
        long_url = Form_[short_code]
        return RedirectResponse(url=long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")