from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_
from models import Note
from schemas import NoteCreate, NoteUpdate
from exceptions import NotFoundException


class NoteService:

    @staticmethod
    def create_note(db: Session, note: NoteCreate):
        new_note = Note(title=note.title, content=note.content)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return {
            "success": True,
            "message": "Note created successfully",
        }

    @staticmethod
    def get_all_notes(db: Session):
        notes = db.query(Note).all()
        return {
            "notes": notes
        }

    @staticmethod
    def get_note_by_id(db: Session, note_id: int):
        if not note_id:
            raise HTTPException(status_code=400, detail="Note ID is required")

        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise NotFoundException("Note not found")

        return note

    @staticmethod
    def update_note(db: Session, note: NoteUpdate):
        note_db = db.query(Note).filter(Note.id == note.id).first()

        if not note_db:
            raise NotFoundException("Note not found")

        note_db.title = note.title
        note_db.content = note.content
        db.commit()
        db.refresh(note_db)
        return {
            "success": True,
            "message": "Note updated successfully",
        }

    @staticmethod
    def delete_note(db: Session, note_id: int):
        note_db = db.query(Note).filter(Note.id == note_id).first()

        if not note_db:
            raise NotFoundException("Note not found")

        db.delete(note_db)
        db.commit()
        return {"message": "Note deleted"}

    @staticmethod
    def search_note(db: Session, query: str):
        if not query:
            # If no query provided, return all notes
            notes = db.query(Note).all()
            return {
                "notes": notes
            }
        note_db = (
            db.query(Note)
            .filter(
                or_(
                    Note.title.contains(query),
                    Note.content.contains(query)
                )
            )
            .all()
        )

        if not note_db:
            raise NotFoundException("Note not found")

        return {
            "notes": note_db,
            "query": query
        }
