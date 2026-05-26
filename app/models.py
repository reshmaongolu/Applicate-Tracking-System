from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Candidate:
    id: int
    name: str
    email: str
    skills: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Job:
    id: int
    title: str
    department: str
    location: str = "Remote"
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Application:
    id: int
    candidate_id: int
    job_id: int
    status: str = "Submitted"
    applied_at: datetime = field(default_factory=datetime.utcnow)
