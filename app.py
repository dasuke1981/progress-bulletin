from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import datetime
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Data store for progress items
progress_items = []
next_id = 1

def calculate_percent(current, max_value):
    if max_value == 0:
        return 0
    return (current / max_value) * 100

def cleanup_old_items():
    global progress_items
    current_time = datetime.datetime.now()
    progress_items = [item for item in progress_items if (current_time - item['timestamp']).days < 7]

def find_item_by_id(item_id):
    for item in progress_items:
        if item['id'] == item_id:
            return item
    return None

@app.post("/add_progress/")
async def add_progress(request: Request, title: str = Form(...), current: int = Form(...), max_value: int = Form(...)):
    global progress_items, next_id
    cleanup_old_items()
    
    existing_item = find_item_by_id(next_id)
    percent = calculate_percent(current, max_value)
    timestamp = datetime.datetime.now()
    
    if existing_item:
        existing_item['title'] = title
        existing_item['current'] = current
        existing_item['max'] = max_value
        existing_item['percent'] = percent
        existing_item['timestamp'] = timestamp
    else:
        progress_items.append({
            'id': next_id,
            'title': title,
            'current': current,
            'max': max_value,
            'percent': percent,
            'timestamp': timestamp
        })
        next_id += 1
    
    return Response(content="Progress added/updated successfully", media_type="text/plain")

@app.get("/")
async def view_progress(request: Request):
    cleanup_old_items()
    return templates.TemplateResponse("progress.html", {"request": request, "progress_items": progress_items})

@app.get("/get_progress/", response_model=list[dict])
async def get_progress():
    cleanup_old_items()
    return progress_items

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
