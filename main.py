from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import hashlib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Form_=[]

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
        Form_.append(url)
        short_code = generate_short_code(url)
        short_url = "https://shorten-url-pyiu.vercel.app/" + short_code
        return templates.TemplateResponse("result.html", {'request': request, "name": short_url})
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    if True:
        return RedirectResponse(url=Form_[0])
    else:
        raise HTTPException(status_code=404, detail="URL not found")
    
