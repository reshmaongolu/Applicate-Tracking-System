from app.models import Candidate, Job, Application


def test_candidate_fields():
    candidate = Candidate(id=1, name="Eve", email="eve@example.com", skills=["JavaScript"])
    assert candidate.id == 1
    assert candidate.email == "eve@example.com"
    assert "JavaScript" in candidate.skills


def test_job_fields():
    job = Job(id=1, title="Frontend Engineer", department="Engineering")
    assert job.title == "Frontend Engineer"
    assert job.department == "Engineering"


def test_application_fields():
    application = Application(id=1, candidate_id=1, job_id=1)
    assert application.status == "Submitted"
    assert application.candidate_id == 1
