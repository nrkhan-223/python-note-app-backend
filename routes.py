from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from note_service import NoteService
from schemas import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter()


# CREATE
@router.post("/create/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return NoteService.create_note(db, note)


# READ ALL
@router.get("/get/notes")
def get_notes(db: Session = Depends(get_db)):
    return NoteService.get_all_notes(db)


# READ ONE
@router.get("/gets/notes/single", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    return NoteService.get_note_by_id(db, note_id)


# UPDATE
@router.put("/update/notes")
def update_note(note: NoteUpdate, db: Session = Depends(get_db)):
    return NoteService.update_note(db, note)


# DELETE
@router.delete("/delete/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return NoteService.delete_note(db, note_id)


# SEARCH NOTES (New endpoint)
@router.get("/search/notes")
def search_notes(
        query: str = Query(..., description="Search query for title or content"),
        db: Session = Depends(get_db)
):
    return NoteService.search_note(db, query)
