from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

notes = {}

@app.post("/notes/")
async def create_note(note: Note):
    note_title = str(len(notes) + 1)
    notes[note_title] = note
    return{"Title": note_title, **note.dict()}

@app.get("/notes/{note_title}")
async def get_note(note_title: str):
    note = notes.get(note_title)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note

@app.put("/notes/{note_title}")
async def update_note(note_title: str, updated_note: Note):
    if note_title not in notes:
        raise HTTPException(status_code=404, detail="Note not found.")
    return updated_note

@app.delete("/notes/{note_title}")
async def delete_note(note_title: str):
    if note_title not in notes:
        raise HTTPException(status_code=404, detail="Note not found.")
    del notes[note_title]
    return {"detail": "Note deleted."}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Note-Taking API."}
    

