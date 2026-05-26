import sqlite3
from datetime import datetime
from typing import List, Optional

from .models import Application, Candidate, Job
from .storage import SQLiteStorage

class ATSService:
    def __init__(self, storage: Optional[SQLiteStorage] = None):
        self.storage = storage or SQLiteStorage()

    def add_candidate(self, name: str, email: str, skills: List[str]) -> Candidate:
        created_at = datetime.utcnow().isoformat()
        self.storage.execute(
            "INSERT INTO candidates (name, email, skills, created_at) VALUES (?, ?, ?, ?)",
            (name, email, ",".join(skills), created_at),
        )
        candidate_id = self.storage.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return Candidate(id=candidate_id, name=name, email=email, skills=skills, created_at=datetime.fromisoformat(created_at))

    def add_job(self, title: str, department: str, location: str = "Remote") -> Job:
        created_at = datetime.utcnow().isoformat()
        self.storage.execute(
            "INSERT INTO jobs (title, department, location, created_at) VALUES (?, ?, ?, ?)",
            (title, department, location, created_at),
        )
        job_id = self.storage.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return Job(id=job_id, title=title, department=department, location=location, created_at=datetime.fromisoformat(created_at))

    def submit_application(self, candidate_id: int, job_id: int) -> Application:
        applied_at = datetime.utcnow().isoformat()
        self.storage.execute(
            "INSERT INTO applications (candidate_id, job_id, status, applied_at) VALUES (?, ?, ?, ?)",
            (candidate_id, job_id, "Submitted", applied_at),
        )
        application_id = self.storage.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return Application(id=application_id, candidate_id=candidate_id, job_id=job_id, status="Submitted", applied_at=datetime.fromisoformat(applied_at))

    def get_candidate(self, candidate_id: int) -> Optional[Candidate]:
        row = self.storage.fetchone("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        return self._candidate_from_row(row) if row else None

    def get_job(self, job_id: int) -> Optional[Job]:
        row = self.storage.fetchone("SELECT * FROM jobs WHERE id = ?", (job_id,))
        return self._job_from_row(row) if row else None

    def list_candidates(self) -> List[Candidate]:
        rows = self.storage.fetchall("SELECT * FROM candidates ORDER BY id")
        return [self._candidate_from_row(row) for row in rows]

    def list_jobs(self) -> List[Job]:
        rows = self.storage.fetchall("SELECT * FROM jobs ORDER BY id")
        return [self._job_from_row(row) for row in rows]

    def list_applications(self) -> List[Application]:
        rows = self.storage.fetchall("SELECT * FROM applications ORDER BY id")
        return [self._application_from_row(row) for row in rows]

    def search_candidates(self, query: str) -> List[Candidate]:
        rows = self.storage.fetchall(
            "SELECT * FROM candidates WHERE name LIKE ? OR email LIKE ? OR skills LIKE ? ORDER BY id",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        return [self._candidate_from_row(row) for row in rows]

    @staticmethod
    def _candidate_from_row(row: sqlite3.Row) -> Candidate:
        skills = row["skills"].split(",") if row["skills"] else []
        return Candidate(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            skills=skills,
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    @staticmethod
    def _job_from_row(row: sqlite3.Row) -> Job:
        return Job(
            id=row["id"],
            title=row["title"],
            department=row["department"],
            location=row["location"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    @staticmethod
    def _application_from_row(row: sqlite3.Row) -> Application:
        return Application(
            id=row["id"],
            candidate_id=row["candidate_id"],
            job_id=row["job_id"],
            status=row["status"],
            applied_at=datetime.fromisoformat(row["applied_at"]),
        )
