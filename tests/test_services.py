import sqlite3
import tempfile
from pathlib import Path

from app.services import ATSService
from app.storage import SQLiteStorage


def test_add_and_list_candidates():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        service = ATSService(storage=SQLiteStorage(str(db_path)))

        candidate = service.add_candidate("Alice", "alice@example.com", ["Python", "Django"])
        assert candidate.id == 1
        assert candidate.name == "Alice"

        candidates = service.list_candidates()
        assert len(candidates) == 1
        assert candidates[0].email == "alice@example.com"


def test_add_job_and_submit_application():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        storage = SQLiteStorage(str(db_path))
        service = ATSService(storage=storage)

        job = service.add_job("Backend Engineer", "Engineering", "Remote")
        candidate = service.add_candidate("Bob", "bob@example.com", ["SQL", "APIs"])
        application = service.submit_application(candidate.id, job.id)

        assert application.id == 1
        assert application.candidate_id == candidate.id
        assert application.job_id == job.id

        applications = service.list_applications()
        assert len(applications) == 1
        assert applications[0].status == "Submitted"


def test_search_candidates():
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        service = ATSService(storage=SQLiteStorage(str(db_path)))

        service.add_candidate("Carol", "carol@example.com", ["Python", "Flask"])
        service.add_candidate("Dave", "dave@example.com", ["Java", "Spring"])

        matches = service.search_candidates("Python")
        assert len(matches) == 1
        assert matches[0].name == "Carol"
