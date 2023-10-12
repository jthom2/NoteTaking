import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import secrets

app = FastAPI()

import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

def load_notes():
    try:
        with open("notes.json", "r") as f:
            data = json.load(f)
            return data.get('data', {})
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_notes(notes):
    with open("notes.json", "w") as f:
        json.dump({"data": notes}, f, indent=4)

@app.post("/notes/")
async def create_note(note: Note):
    notes = load_notes()
    note_id = secrets.token_hex()
    notes[note_id] = note.dict()
    save_notes(notes)
    return {"id": note_id, **note.dict()}

@app.get("/notes/{note_id}")
async def get_note(note_id: str):
    notes = load_notes()
    note = notes.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note

@app.put("/notes/{note_id}")
async def update_note(note_id: str, updated_note: Note):
    notes = load_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found.")
    notes[note_id] = updated_note.dict()
    save_notes(notes)
    return updated_note

@app.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    notes = load_notes()
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found.")
    del notes[note_id]
    save_notes(notes)
    return {"detail": "Note deleted."}                  


        


@app.get("/")
def read_root():
    return {"message": "Cream"}

origins = [
    "https://jthom-note-taker-d63b752b7b0c.herokuapp.com",
    # other origins you want to allow can be added here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
