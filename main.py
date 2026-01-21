from fastapi import FastAPI, Depends
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from exception_handlers import custom_exception_handler, validation_exception_handler
from exceptions import NotFoundException, CustomException
from models import Base, Note
from schemas import NoteCreate, NoteResponse, NoteUpdate

from fastapi import HTTPException

from typing import List
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@app.post("/create/notes", )
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {
        "success": True,
        "message": "Note created successfully",
    }


# READ ALL
class NotesListResponse(BaseModel):
    notes: List[NoteResponse]


@app.get("/get/notes", response_model=NotesListResponse)
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return {
        "notes": notes
    }


# READ ONE
@app.get("/gets/notes/single", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    if not note_id:
        raise HTTPException(status_code=400, detail="Note ID is required")

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise NotFoundException("Note not found")

    return note


# UPDATE
@app.put("/update/notes", )
def update_note(note: NoteUpdate, db: Session = Depends(get_db)):
    note_db = db.query(Note).filter(Note.id == note.id).first()
    note_db.title = note.title
    note_db.content = note.content
    db.commit()
    db.refresh(note_db)
    return {
        "success": True,
        "message": "Note Update successfully",
    }


# DELETE
@app.delete("/delete/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note_db = db.query(Note).filter(Note.id == note_id).first()
    db.delete(note_db)
    db.commit()
    return {"message": "Note deleted"}
